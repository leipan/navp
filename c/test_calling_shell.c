#include <stdio.h>
#include <stdlib.h>

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


int main(void) {

  /* char *cmd = "curl http://higgs.jpl.nasa.gov:8080/svc/navp_hop 1>&2"; */
  char *cmd = "curl http://higgs.jpl.nasa.gov:8080 1>&2";

  call_shell_command(cmd);

  return 0;
}
