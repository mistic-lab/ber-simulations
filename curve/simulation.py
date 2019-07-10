import os
import sys
from results import BERCurveResults

class BERCurveSimulation(object):
    def __init__(self,simulation,in_memory=False,results_dict=None,results_dir="",file_name=None):
        self.simulation = simulation
        self.in_memory = in_memory
        self.results_dir = results_dir
        file_path = self.get_file_path(file_name) if in_memory == False else None
        self.results = BERCurveResults(file_name=file_path,results_dict=results_dict)

    def get_file_path(self,file_name=None):
        if file_name is None:
            file_name = "ber-sim-%s.csv" % self.simulation.title.lower().replace(' ','-')
        return os.path.normpath(os.path.join(self.results_dir,file_name))

    def load(self):
        self.results.load() 

    @property
    def title(self):
        return self.simulation.title

    def get_simulations_needed(self,ebno_dbs=[],number_of_sims=1):
        # Create an entry for each simulation remaining (difference between number in results and number of sims requested)
        simulations_needed = [sim for sims in [[ebno_db]*(number_of_sims-len(self.results.get_ebno_results(ebno_db))) for ebno_db in ebno_dbs] for sim in sims]
        return simulations_needed  
    
    def run(self,ebno_db,on_progress=None):
        # Send out initial progress
        on_progress(0)
        ber,total_errors = self.simulation.measure_ber(
            ebno_db,
            on_progress
        )
        
        self.results.set_result({
            'ber':ber,
            'total_errors':total_errors,
            'ebno_db':ebno_db
        })        
        self.results.save()

    def get_bers(self,ebno_dbs):
        ebnos,bers = self.results.get_average_ebno_ber_values()
        indexes = [i for i,v in enumerate(ebnos) if v in ebno_dbs]
        return [bers[i] for i in indexes] 