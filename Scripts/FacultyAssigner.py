import numpy as np
import pandas as pd
import random
import Scripts.PopUpManager as PopUpManager
import time


class FacultyAssigner:
    def __init__(self, input_file_path, destination, root, progress):
        self.function = progress
        self.root = root
        self.input_file_path = input_file_path
        self.destination = destination
        self.df = pd.read_csv(input_file_path)
        self.faculty_list = list(self.df.Faculty)
        df = self.df.dropna()
        self.dates = list(df.Dates)
        self.slot1 = list(df.Slot1)
        self.slot2 = list(df.Slot2)
        self.max_occurrence = ((sum(self.slot1) + sum(self.slot2)) // len(self.faculty_list)) + 1
        self.faculty_key = {}
        for i in self.faculty_list:
            self.faculty_key[i] = 0

    def get_slot(self, slot):
        df = pd.DataFrame({})
        for i in range(len(self.dates)):
            data = []
            for _ in range(int(slot[i])):
                choice = None
                while choice is None:
                    faculty = random.choice(self.faculty_list)
                    if (self.faculty_key[faculty] < self.max_occurrence) and (faculty not in data):
                        self.faculty_key[faculty] += 1
                        choice = faculty
                    else:
                        continue
                if choice is None:
                    PopUpManager.error_popup(self.root, 'Some unexpected error occurred')
                else:
                    data.append(choice)
            for y in range(len(self.faculty_list)-len(data)):
                data.append(np.nan)
            df[self.dates[i]] = data
        time.sleep(1)

        return df

    def generate_check_file(self, slot):
        df = pd.DataFrame({}, columns=self.dates, index=self.faculty_list)
        for i in self.dates:
            for j in self.faculty_list:
                if j in list(slot[i]):
                    df[i][j] = 'X'
                else:
                    df[i][j] = np.nan
        return df

    def runner(self):
        slot1 = self.get_slot(self.slot1)
        slot2 = self.get_slot(self.slot2)
        file1 = self.generate_check_file(slot1)
        file2 = self.generate_check_file(slot2)
        file1.to_excel(self.destination+'/Slot1.xlsx')
        file2.to_excel(self.destination+'/Slot2.xlsx')
        self.function()
