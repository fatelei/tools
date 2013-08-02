#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>

int read_dir(char *pth) {
    char path[100];
    char tmp_path[300];
    char cmd[1000];
    DIR *dir;
    struct dirent *file;
    memset(path, 0x0, sizeof(path));
    strncpy(path, pth, strlen(pth));
    if ((dir = opendir(path)) != NULL) {
        while ((file = readdir(dir)) != NULL) {
            if (strcmp(file->d_name, ".") == 0 || strcmp(file->d_name, "..") == 0) {
                continue;
            } else {
                if (strnstr(file->d_name, ".", 1) == NULL) {
                    memset(tmp_path, 0x0, sizeof(tmp_path));
                    memset(cmd, 0x0, sizeof(cmd));
                    strncpy(tmp_path, path, strlen(path));
                    strncat(tmp_path, "/", 1);
                    strncat(tmp_path, file->d_name, strlen(file->d_name));
                    sprintf(cmd, "echo \"`sed 's/,//g' %s`\" > %s", tmp_path, tmp_path);
                    printf("cmd: %s\n", cmd);
                    system(cmd);
                }
            }
        }
    } else {
        printf("can't open dir: %s\n", path);
        return 1;
    }
}


int main(int argc, char *argv[]) {
    read_dir(argv[1]);
    return 0;
}

