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
#include <unistd.h>
#include <sys/types.h>

#include "dmtcp.h"


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



int hop(int original_generation, int port) {
  int retval = dmtcp_checkpoint();
  if (retval == DMTCP_AFTER_CHECKPOINT) {
    // Wait long enough for checkpoint request to be written out.
    while (dmtcp_get_generation() == original_generation) {
      sleep(1);
    }

    printf("*** dmtcp_checkpoint: This program has now invoked a checkpoint.\n"
           "      It will resume its execution next.\n");
    get_process_pid();
    printf("let navp daemon take care of restart now. exiting ...\n");
    // call the NAVP hop service
    // char *restart_cmd = "/home/leipan/projects/dmtcp/git/navp/c/dmtcp_restart_script.sh 1>&2";
    // char *restart_cmd = "curl http://higgs.jpl.nasa.gov:8080/svc/hop 1>&2 &";
    char restart_cmd[256];
    sprintf(restart_cmd, "curl http://higgs.jpl.nasa.gov:8080/svc/hop?port=%d 1>&2", port);
    call_shell_command(restart_cmd);

    exit (0);
  } else if (retval == DMTCP_AFTER_RESTART) {
    printf("*** dmtcp_checkpoint: This program is now restarting.\n");
  } else if (retval == DMTCP_NOT_PRESENT) {
    printf(" *** dmtcp_checkpoint: DMTCP is not running."
           "  Skipping checkpoint.\n");
  }

  printf("\n*** Process done executing.  Successfully exiting.\n");
  if (retval == DMTCP_AFTER_CHECKPOINT) {
    printf("*** Execute ./dmtcp_restart_script.sh to restart.\n");
  }

  return 0;
}

int main()
{
  int dmtcp_enabled = dmtcp_is_enabled();

  if (!dmtcp_enabled) {
    printf("\n *** dmtcp_is_enabled: False. Run executable under dmtcp_launch.\n\n");
    exit(0);
  }

  int original_generation;
  if (dmtcp_enabled) {
    original_generation = dmtcp_get_generation();
  }

  int port;

  int l1 = 5;
  int l2 = 10;
  int l3 = 15;

  // print out in the 1st loop
  int i;
  for (i=0; i<l1; i++) {
    printf("%d ", i);
  }
  printf("\n");

  port = 7788;
  int r1 = hop(original_generation, port);

  // print out in the 2nd loop
  for (i=l1; i<l2; i++) {
    printf("%d ", i);
  }
  printf("\n");

  port += 1;
  int r2 = hop(original_generation, port);

  // print out in the 2nd loop
  for (i=l2; i<l3; i++) {
    printf("%d ", i);
  }
  printf("\n");

  return 0;
}
