// # gcc -o nvml_test nvml_test.c -I /usr/include/nvidia/gdk -l nvidia-ml -std=c99

#include <stdio.h>
#include <unistd.h>
#include <assert.h>
#include <strings.h>
#include <string.h>

#include <nvml.h>

int main(int argc, char *argv[]) {
 unsigned int count;
 assert( nvmlInit() == NVML_SUCCESS );
 assert( nvmlDeviceGetCount(&count) == NVML_SUCCESS );

 if ((argc == 2) && (!strcmp(argv[1], "restart"))) {
  for(int i=0; i<count; i++) {
   nvmlDevice_t device;

   assert( nvmlDeviceGetHandleByIndex ( i, &device) == NVML_SUCCESS );

   char name[NVML_DEVICE_NAME_BUFFER_SIZE];
   assert( nvmlDeviceGetName ( device, name, sizeof(name) ) == NVML_SUCCESS );

   // clear statistics
   assert( nvmlDeviceSetAccountingMode( device, NVML_FEATURE_DISABLED) == NVML_SUCCESS );
   assert( nvmlDeviceSetAccountingMode( device, NVML_FEATURE_ENABLED) == NVML_SUCCESS );
 
   nvmlEnableState_t e_pers;
   assert( nvmlDeviceGetPersistenceMode (device, &e_pers) == NVML_SUCCESS );

   nvmlEnableState_t e_acct;
   assert( nvmlDeviceGetAccountingMode (device, &e_acct) == NVML_SUCCESS );
   printf("gpu[%d] '%s' %s%s\n", i, name, e_acct?"accounting ":"", e_pers?"persistent":"");
  }
 }

 // header
 printf("%4s %4s %4s %4s %6s\n", "id", "pid", "gpu%", "mem%", "memsz");

 while(1) {
  for(int i=0; i<count; i++) {
   nvmlDevice_t device;
   assert( nvmlDeviceGetHandleByIndex ( i, &device) == NVML_SUCCESS );

   nvmlMemory_t mem;
   assert( nvmlDeviceGetMemoryInfo (device, &mem)== NVML_SUCCESS );

   nvmlUtilization_t util;
   assert( nvmlDeviceGetUtilizationRates ( device, &util) == NVML_SUCCESS );

   // global statistics
   printf("%4d %4s %4d %4d %6d\n", i, "-", util.gpu, util.memory, mem.used/1024/1024);

   unsigned int pa_count=64;
   unsigned int pa[64];
   assert( nvmlDeviceGetAccountingPids( device, &pa_count, pa ) == NVML_SUCCESS );
   for(int j=0; j<pa_count; j++) {
     nvmlAccountingStats_t stat;
     assert ( nvmlDeviceGetAccountingStats (device, pa[j], &stat) == NVML_SUCCESS );
     // per process accounting (cumulative) statistics 
     printf("%4d %4d %4d %4d %6d\n", i, pa[j], stat.gpuUtilization, stat.memoryUtilization, stat.maxMemoryUsage/1024/1024);
   }
  }
  fflush(stdout);
  sleep(1);
 }

 assert( nvmlShutdown() == NVML_SUCCESS );
 return 0;
}
