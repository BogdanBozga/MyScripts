#!/usr/bin/env python3
"""
This is a script that remove the AA_JungleliskEggFertilized, spider eggs that
don't have a pointer to any real data, they are junk junk that make lag and
don't affect the story
"""
import re, logging, shutil, sys, os

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.info('SCRIPT RUNNING')

source = '/home/bogdan/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves/'
destination = '/home/bogdan/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves/'
destinationBackup = '/home/bogdan/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves/'


file_name = "Red Thumbos Faction (Permadeath).rws"
temp_file_name = "temporal.rws"
destination = destination + temp_file_name
source = source + file_name
destinationBackup = destinationBackup + "Backup " + file_name

logging.info('CREATING BACKUP...')
shutil.copyfile(source, destinationBackup)
logging.info('BACKUP DONE!;)')



#input file
fin = open(source, "rt")
#output file to write the result to
fout = open(destination, "wt")

logging.info('Cretaing variable for execution')
find_counter = 0
find_eggs_counter = 0
number_lines = 0
posible_find = False
backup_line =''
in_remove_egg_mode = False





for line in fin:
    number_lines  = number_lines + 1
	#remove the whitespace and \n from the line
    line_edited = re.sub(r'\s+', '', line)
    if in_remove_egg_mode:
        if line_edited == '</thing>':
            in_remove_egg_mode = False
            logging.info('  remove finish')
        elif '<stackCount>' in line_edited:
            logging.info('      increase egg stack counter')
            line_edited = line_edited.replace('<stackCount>','')
            line_edited = line_edited.replace('</stackCount>','')
            find_eggs_counter = find_eggs_counter + int(line_edited)
    else:
        if line_edited == '<thingClass="ThingWithComps">':
            logging.info('thing Class --found')
            posible_find = True
            backup_line = line
        elif posible_find:
            if line_edited == '<def>AA_JungleliskEggFertilized</def>':
                logging.info(f'      egg entry --found --begin deleting')
                in_remove_egg_mode = True
                find_counter = find_counter + 1
            else:
                logging.info('thing Class --found --false found')
                fout.write(backup_line)
                fout.write(line)
                posible_find = False
        else:
    	       fout.write(line)







#close input and output files

fin.close()
fout.close()



logging.info("Renamin files")
logging.info(f'rm \"{source}\"')
os.system(f'rm \"{source}\"')
os.system(f'mv \"{destination}\" \"{source}\"')



logging.info('ALL DONE, HAVE FUN PLAYING RIMWORL, HERE HAVE SOME DATA ABOUT WHAT I HAVE DONE')
logging.info(f'Total initial lines {number_lines}')
logging.info(f'Total entry found {find_counter}')
logging.info(f'Total eggs removed {find_eggs_counter}')



# #Below code mompare the size before and after the script execution
# def _count_generator(reader):
#     b = reader(1024 * 1024)
#     while b:
#         yield b
#         b = reader(1024 * 1024)
# initial_lines  = 0
# with open(r'rimsave.rws', 'rb') as fp:
#     c_generator = _count_generator(fp.raw.read)
#     # count each \n
#     count = sum(buffer.count(b'\n') for buffer in c_generator)
#     initial_lines = count+1
#     logging.info(f'Total initial lines: {count + 1}')
#
# final_lines  = 0
#
# with open(r'out.rws', 'rb') as fp:
#     c_generator = _count_generator(fp.raw.read)
#     # count each \n
#     count = sum(buffer.count(b'\n') for buffer in c_generator)
#     final_lines = count+1
#     logging.info(f'Total final lines:{count + 1}')
#
# logging.info(f"Difference {initial_lines-final_lines}")
