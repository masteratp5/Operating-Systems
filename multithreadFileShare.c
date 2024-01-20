#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

char fileName[20]; //name of input file
int bufferSize;//size of buffer

void *threadFunction(void *arg) {
  FILE *fp;
  FILE *fout;
  char outputFile[20]; // name of output file
  char buffer[bufferSize];

  // append thread number to the name of the output files
  sprintf(outputFile, "step5_Output%d.txt", (int)arg);

  fp = fopen(fileName, "rb");  // Open file in binary mode for fread
  if (fp == NULL) {
    perror("Error opening input file");
    exit(EXIT_FAILURE);
  }

  fout = fopen(outputFile, "wb");  // Open file in binary mode for fwrite
  if (fout == NULL) {
    perror("Error opening output file");
    exit(EXIT_FAILURE);
  }

  // read the input file's contents into buffer
  size_t bytesRead;
  while ((bytesRead = fread(buffer, sizeof(char), bufferSize, fp)) > 0) {
    // write the buffer's contents into the outputFile
    fwrite(buffer, sizeof(char), bytesRead, fout);
  }

  fclose(fp);
  fclose(fout);
  return NULL;
}

int main (int argc, char *argv[]){
  bufferSize = atoi(argv[2]);  //buffersize
  int NTHREADS = atoi(argv[3]); //number of threads

  pthread_t threads[NTHREADS]; //array of threads
  strcpy(fileName, argv[1]);

  int i;
  //create threads
  for (i = 0; i < NTHREADS; i++) {
    pthread_create(&threads[i], NULL, threadFunction, (void *)(size_t)i);
	}
  // close threads
  for (i = 0; i < NTHREADS; i++) {
    pthread_join(threads[i],NULL);
  }
  return 0;
}
