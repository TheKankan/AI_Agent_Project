from functions.get_files_info import get_files_info

print(get_files_info("calculator")) #testing working directory

print("\n______________________________________________________________\n")

print(get_files_info("fakecalc")) #testing fake working directory : should error

print("\n______________________________________________________________\n")

print(get_files_info("calculator", "pkg")) #testing directory withing the working directory

print("\n______________________________________________________________\n")

print(get_files_info("calculator", "/bin")) #testing outside working directory : should error

print("\n______________________________________________________________\n")

print(get_files_info("calculator", "../")) #testing outside working directory : should error

print("\n______________________________________________________________\n")

print(get_files_info("calculator", "doesntexist")) #testing with a directory that shouldn't exist : should error