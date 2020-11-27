#include <stdio.h>
#include <stdlib.h>

int main(void) {
/* ls -al | grep '^d' */
  FILE *pp;
  pp = popen("curl http://higgs.jpl.nasa.gov:8080/svc/navp_hop 1>&2", "r");
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
