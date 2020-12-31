#include <libgen.h>
#define _GNU_SOURCE 
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

int main(int argc, char const *argv[])
{
  const char* local_file = "/home/leipan/foo/bar/baz.txt";
  char* dummy = strdup(local_file);
  char* dummy2 = strdup(local_file);

  char* dname = dirname(dummy);
  char* fname = basename(dummy2);

  // use dir and filename now
  printf("dname: %s\n", dname);
  printf("fname: %s\n", fname);

  return 0;
}
