import os
import sys
import csv

class BERCurveResults(object):
    def __init__(self,file_name=None,results_dict=None):
        object.__init__(self)
        self.file_name = file_name        
        self.results = results_dict if results_dict is not None else {}
    
    def load(self):
        if self.file_name is not None:
            try:
                with open(self.file_name,mode='r') as csv_file:
                    reader = csv.DictReader(csv_file)
                    line_count=0
                    print("Loading results from previous run")
                    for row in reader:
                        result = {
                            'ebno_db':float(row["ebno_db"]),
                            'total_errors':int(row["total_errors"]),
                            'ber':float(row["ber"])
                        }
                        self.set_result(result)
                        line_count = line_count + 1
                    print("Loaded",line_count,"saved results")
            except IOError:
                print("No recorded data found")

    def save(self):
        if self.file_name is not None:
            results_dir = os.path.dirname(self.file_name)
            if not os.path.exists(results_dir):
                print("Creating directory %s"%results_dir)
                os.makedirs(results_dir)
            with open(self.file_name,mode='w+') as csv_file:
                writer = csv.DictWriter(csv_file,fieldnames=['ebno_db','total_errors','ber']) 
                writer.writeheader()
                recorded_rows = self.get_results_list()
                writer.writerows(recorded_rows)
                print("Saved",len(recorded_rows),"results to",self.file_name)

    def set_result(self,result):
        entry = result.copy()
        ebno_db = result['ebno_db']
        values = []
        if ebno_db in self.results.keys():            
            values = self.results[ebno_db]    
        values.append(entry)
        self.results[ebno_db]=values
    
    def get_ebno_results(self,ebno_db):
        return self.results[ebno_db] if ebno_db in self.results.keys() else []

    def get_results_list(self):
        return [item for items in [val for key,val in sorted(self.results.copy().iteritems())] for item in items]

    def get_average_ebno_ber_values(self):
        results = self.results.copy()
        ebno_dbs = sorted(results.keys())
        ber_vals = [sum(bers)/len(bers) for bers in [map(lambda x:x['ber'],results[ebno_db]) for ebno_db in ebno_dbs]]
        return ebno_dbs,ber_vals