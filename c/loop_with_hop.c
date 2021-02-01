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


void swap_ips(char x[], char y[]) {

   char temp[256];
   strcpy(temp, x);
   strcpy(x, y);
   strcpy(y, temp);
}


int call_shell_command(char *shell_command) {
/* ls -al | grep '^d' */
  FILE *pp;
  /* pp = popen("curl http://higgs.jpl.nasa.gov:8080/svc/navp_hop 1>&2", "r"); */
  pp = popen(shell_command, "r");
  if (pp != NULL) {
    while (1) {
      char *line;
      char buf[1000];
      line = fgets(buf, sizeof buf, pp);
      if (line == NULL) break;
      if (line[0] == 'd') printf("%s", line); /* line includes '\n' */
    }
    pclose(pp);
  }
  return 0;
}


int get_process_pid() {
  pid_t pid, ppid;
  gid_t gid;

  /* get the process id */
  if ((pid = getpid()) < 0) {
    perror("unable to get pid");
    return -1;
  } else {
    printf("--- The process id is %d\n", pid);
    return pid;
  }

  return -1;
}



int hop(int original_generation, char *src_ip, char *dst_ip, int port) {

  const char *ckpt_filename;

  int retval = dmtcp_checkpoint();
  if (retval == DMTCP_AFTER_CHECKPOINT) {
    // Wait long enough for checkpoint request to be written out.
    while (dmtcp_get_generation() == original_generation) {
      sleep(1);
    }

    printf("ckpt filename: \n");
    ckpt_filename = dmtcp_get_ckpt_filename();
    printf("%s\n", ckpt_filename);

    // printf("*** dmtcp_checkpoint: This program has now invoked a checkpoint.\n"
    //        "      It will resume its execution next.\n");
    // get_process_pid();
    // printf("let navp daemon take care of restart now. exiting ...\n");
    // call the NAVP hop service
    // char *restart_cmd = "/home/leipan/projects/dmtcp/git/navp/c/dmtcp_restart_script.sh 1>&2";
    // char *restart_cmd = "curl http://higgs.jpl.nasa.gov:8080/svc/hop 1>&2 &";
    char restart_cmd[256];
    sprintf(restart_cmd, "curl \"http://%s:8080/svc/hop?src_ip=%s&dst_ip=%s&ckpt=%s&port=%d\" 1>&2", dst_ip, src_ip, dst_ip, ckpt_filename, port);
    printf("--- restart_cmd: %s\n", restart_cmd);
    call_shell_command(restart_cmd);

    // char *my_ip = get_ip();
    // printf("--- my ip is %s\n", my_ip);

    exit (0);
  } else if (retval == DMTCP_AFTER_RESTART) {
    printf("*** dmtcp_checkpoint: This program is now restarting.\n");
  } else if (retval == DMTCP_NOT_PRESENT) {
    // printf(" *** dmtcp_checkpoint: DMTCP is not running."
    //       "  Skipping checkpoint.\n");
  }

  // printf("\n*** Process done executing.  Successfully exiting.\n");
  if (retval == DMTCP_AFTER_CHECKPOINT) {
    printf("*** Execute ./dmtcp_restart_script.sh to restart.\n");
  }

  return 0;
}


// This program will hop between src_ip ('weather') and dst_ip ('higgs')
// as it prints out numbers. To run it:
// curl "http://weather.jpl.nasa.gov:8080/svc/ingest?exe=/home/leipan/projects/dmtcp/git/navp/c/loop_with_hop"
// note: make sure the NAVP Bridging Services are running on both servers

int main()
{
  int dmtcp_enabled = dmtcp_is_enabled();
  char src_ip[256] = "weather2.jpl.nasa.gov";
  char dst_ip[256] = "higgs.jpl.nasa.gov";
  char ip1[256];
  int port=7788, r1, i, loop_bound = 20;
  int original_generation;

  get_ip(&ip1);
  // printf("ip1: %s\n", ip1);
  
  if (strcmp(ip1, src_ip) != 0) {
    // printf("calling swap() ...\n");
    swap_ips(src_ip, dst_ip);
  } 

  printf("src_ip: %s\n", src_ip);
  printf("dst_ip: %s\n", dst_ip);

  if (!dmtcp_enabled) {
    printf("\n *** dmtcp_is_enabled: False. Run executable under dmtcp_launch if you want to hop among servers.\n\n");
  }
  else {
    original_generation = dmtcp_get_generation();
  }


  for (i=0; i<loop_bound; i++) {
    printf("%d ", i);

    if ((i+1)%5 == 0) {
      printf("\n");
      port += 1;
      r1 = hop(original_generation, src_ip, dst_ip, port);

      // swap the src and dst so we can hop back
      swap_ips(src_ip, dst_ip);
    }
  }

  return 0;
}
