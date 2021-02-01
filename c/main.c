/* NOTE: This file must be compiled with -fPIC in order to work properly.
 *
 *       The code in this file will work both with and without DMTCP.
 *       Of course, the dmtcp.h file is needed in both cases.
 *
 * These functions are in <DMTCP_ROOT>/lib/dmtcp/libdmtcp.so and dmtcp.h
 *   int dmtcp_is_enabled() - returns 1 when running with DMTCP; 0 otherwise.
 *   int dmtcp_checkpoint() - returns DMTCP_AFTER_CHECKPOINT,
 *                                   DMTCP_AFTER_RESTART, or DMTCP_NOT_PRESENT.
 * These return 0 on success and DMTCP_NOT_PRESENT if DMTCP is not present.
 *   int dmtcp_disable_ckpt() - DMTCP will block any checkpoint requests.
 *   int dmtcp_enable_ckpt() - DMTCP will execute any blocked
 *               checkpoint requests, and will permit new checkpoint requests.
 *
 * FOR ADVANCED USERS, ONLY:
 *   dmtcp_get_local_status
 *   dmtcp_get_coordinator_status
 *   dmtcp_install_hooks
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

#include "dmtcp.h"

void get_ip();

void swap_ips(char x[], char y[]) {

   char temp[256];
   strcpy(temp, x);
   strcpy(x, y);
   strcpy(y, temp);
}


int main()
{
  char ip1[256];
  char src_ip[256] = "weather.jpl.nasa.gov";
  char dst_ip[256] = "higgs.jpl.nasa.gov";

  printf("src_ip: %s\n", src_ip);
  printf("dst_ip: %s\n", dst_ip);

  get_ip(&ip1);
  printf("ip1: %s\n", ip1);

  if (strcmp(ip1, src_ip) != 0) {
    printf("calling swap() ...\n");
    swap_ips(src_ip, dst_ip);
  }

  printf("src_ip: %s\n", src_ip);
  printf("dst_ip: %s\n", dst_ip);

  return 0;
}
