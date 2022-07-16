#!/usr/bin/python3

import json
import glob
# Import statistics Library
import statistics
import time
from operator import itemgetter
from multiprocessing import Pool
from deco import concurrent, synchronized

# Make an empty list to store the values from json files
eva_list = []
eva_new_list = []
targets_list = []
disease_list = []
eva_unmodified_list = []
value_list = []


def import_targets_data():
    start_time = time.time()
    target_files = glob.glob("targets/*.json")
    for jsonFile in target_files:
        with open(jsonFile) as f:
            for jsonObj in f:
                targets_dict = json.loads(jsonObj)
                targets_list.append(targets_dict)

    print("--- %s seconds --- importing targets data" %
          (time.time() - start_time))


def import_diseases():
    start_time = time.time()
    disease_files = glob.glob("diseases/*.json")
    for jsonFile in disease_files:
        with open(jsonFile) as f:
            for jsonObj in f:
                disease_dict = json.loads(jsonObj)
                disease_list.append(disease_dict)
    print("--- %s seconds --- importing disease data" %
          (time.time() - start_time))


def import_eva_data():
    print("Started importing Eva data")
    # List all the files with etension .json from the folder
    eva_files = glob.glob("part*.json")
    start_time = time.time()
    for jsonFile in eva_files:
        with open(jsonFile) as f:
            for jsonObj in f:
                eva_dict = json.loads(jsonObj)
                eva_list.append(eva_dict)
    print("--- %s seconds --- importing eva data" % (time.time() - start_time))
    # create a clone of the list to use later
    eva_unmodified_list.extend(eva_list)


def loop_eva_data():
    print("Looping over eva data now")
    #Checking timeit takes in seconds -- Quite high for now almost 1 hr
    start_time = time.time()
    # Loop through our eva_list using for loop
    for eva_unique in eva_list:
        # Only continue with the code down if our value is not null
        if eva_unique is not None:
            # create several lists for storage below
            median_list = []
            top3 = []
            eva_sub_list = {}
            eva_sub_list["targetId"] = eva_unique["targetId"]
            eva_sub_list["diseaseId"] = eva_unique["diseaseId"]
            search = [eva_unique["targetId"], eva_unique["diseaseId"]]
            for index, sublist in enumerate(eva_list):
                # second loop (n*n) Loop only when sublist is not null
                if sublist is not None and search == [
                        sublist["targetId"], sublist["diseaseId"]
                ]:
                    # Add the score to a list for purposes of median and top3 calculations
                    median_list.append(sublist["score"])
                    eva_list[index] = None
            # calculate median score
            eva_sub_list["median"] = statistics.median(median_list)
            # sort the mid=edian score in reverse and then pick the first 3
            median_list.sort(reverse=True)
            for index2, top_median in enumerate(median_list):
                if index2 > 2:
                    break
                top3.append(top_median)

            eva_sub_list["top3"] = top3
            eva_new_list.append(eva_sub_list)

    print("--- %s seconds --- indexing and giving results" %
          (time.time() - start_time))


def join_on_targets():
    print("Started Join on targets")
    for index, eva_value in enumerate(eva_new_list):
        search = eva_value["targetId"]
        targets_dict = {}
        for target in targets_list:
            if search == target["id"]:
                targets_dict["approvedSymbol"] = target["approvedSymbol"]
                eva_new_list[index].update(targets_dict)
                #print(eva_new_list[index])
                break


def join_on_diseases():
    print("Started Join on diseases")
    for index, eva_value in enumerate(eva_new_list):
        search = eva_value["diseaseId"]
        disease_dict = {}
        for disease in disease_list:
            if search == disease["id"]:
                disease_dict["name"] = disease["name"]
                eva_new_list[index].update(disease_dict)
                break


def sort_eva_list(list_to_sort):
    print("Started sorting")
    return sorted(eva_new_list, key=itemgetter('median'))


def count_targets_pair(unmodified_list):
    print("Started the target target pairs")
    start_time = time.time()
    #Extract targetId and diseaseId, we are just interested in those
    modified_list = []
    count = 0
    for value in unmodified_list:
        value_list = []
        value_list.append(value["targetId"])
        value_list.append(value["diseaseId"])
        modified_list.append(value_list)

    # Start finding target-target pairs connected to atleast 2 diseases, we want a combination of (AC,BC,AD,BD) target disease pair
    for index, target_disease in enumerate(modified_list):

        #Start with AC
        targetA = target_disease[0]
        diseaseC = target_disease[1]
        targetB = search_BC(modified_list, targetA, diseaseC)
        # if AC found, find BC
        if targetB != None:

            diseaseD = search_AD(modified_list, targetA, diseaseC)
            #if BC found, find AD
            if diseaseD != None:

                pair_target = search_BD(modified_list, targetB, diseaseD)
                # All good so far, if AD returns true then we have found a two set of targets(AB) linked to atleast 2 diseases (CD)
                if pair_target:
                    count += 1
                    modified_list[index] = None

    print("--- %s seconds --- for counting target-target pairs" %
          (time.time() - start_time))
    return count


def search_BC(modified_list, targetA, diseaseC):
    for td_list in modified_list:
        if td_list != None:
            targetB = td_list[0]
            if diseaseC == td_list[1] and targetB != targetA:
                return targetB
    return


def search_AD(modified_list, targetA, diseaseC):
    for td_list in modified_list:
        if td_list != None:
            diseaseD = td_list[1]
            if targetA == td_list[0] and diseaseD != diseaseC:
                return diseaseD
    return


def search_BD(modified_list, targetB, diseaseD):
    for td_list in modified_list:
        if td_list != None:
            if td_list[0] == targetB and td_list[1] == diseaseD:
                return True
    return


if __name__ == "__main__":
    import_eva_data()
    import_targets_data()
    import_diseases()
    print("Done importing!")
    loop_eva_data()
    # with Pool(5) as p:
    #     p.map(loop_eva_data, eva_list)
    join_on_targets()
    join_on_diseases()
    sorted_list_of_dict = sort_eva_list(eva_new_list)
    target_target_pairs = count_targets_pair(eva_unmodified_list[1:10000])
    print("Target target pairs are ", target_target_pairs)
