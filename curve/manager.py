import os
import sys
import traceback
import time
from simulation import BERCurveSimulation
from multiprocessing import Process, JoinableQueue, Manager,cpu_count, Value


class BERSimulationManager(object):
    """
    BER Curve Simulation Manager
    """
    def __init__(self, ebno_dbs, number_of_sims,results_dir=""):
        self.results_dir = results_dir
        self.curveSimulations = []
        self.ebno_dbs = ebno_dbs
        self._manager = Manager()
        self.progress = self._manager.dict()
        self.work_queue = JoinableQueue()
        self.number_of_sims = number_of_sims
        self.__sim_map = {}

    def add_simulation(self,simulation,in_memory=True):
        self.curveSimulations.append(
            BERCurveSimulation(
                simulation,
                in_memory=in_memory,
                results_dict=self._manager.dict(),
                results_dir=self.results_dir
                )
        )
        
    def get_num_simulations_remaining(self):
        return len(self.progress.keys())+self.work_queue.qsize()

    def remove_progress(self,id):
        if id in self.progress.keys():
            del self.progress[id]

    def handle_progress(self,id,progress):   
        self.progress[id]= progress

    @property
    def simulations_remaining(self):
        return len(self.progress.keys())+self.work_queue.qsize()

    def run_simulation(self,work_q):
        while not work_q.empty():
            work = work_q.get()
            ebno_db = work["ebno_db"]
            sim_id = work["id"]
            curveSim = self.__sim_map[sim_id]

            try:
                print("Simulation Started (ebno_db=%f)" % ebno_db)
                curveSim.run(ebno_db,on_progress=lambda t:self.handle_progress(sim_id,{'ebno_db':ebno_db,'total_errors':t}))
                self.remove_progress(sim_id)
                print("Simulation Finished (ebno_db=%f)" % ebno_db)
                work_q.task_done()
            except Exception as err:
                # Put the work back on the queue
                print("Simulation %d Failed (ebno_db=%f)\r\n" % (sim_id,ebno_db))
                traceback.print_exception(*sys.exc_info())
                work_q.put(work)
                self.remove_progress(sim_id)
                
        return True

    def build_work_queue(self):
        total_simulations = []
        for curve in self.curveSimulations:
            curve.simulation.initialize()
            curve.load()
            simulations_needed = curve.get_simulations_needed(self.ebno_dbs,self.number_of_sims)
            [total_simulations.append({'sim':curve,'ebno_db':x}) for x in simulations_needed]
        
        # Create work queue and add the needed simulations
        self.work_queue = JoinableQueue(maxsize=len(total_simulations))
        for i,x in enumerate(total_simulations):
            self.__sim_map[i] = x['sim']
            self.work_queue.put({'id':i,'ebno_db':x['ebno_db']})

    def start_workers(self,num_workers):
        print("Starting %d worker processes" % num_workers)     
        for i in range(min(num_workers,cpu_count())):
            worker = Process(target=self.run_simulation,args=(self.work_queue,))
            worker.daemon = True
            worker.start()

    def generate_curves(self,num_processes=cpu_count(),print_status=True):
        self.build_work_queue()
        total_runs = self.simulations_remaining
        if(total_runs > 0):
            self.start_workers(num_processes)
            try:
                while True:
                    
                    num_remaining = self.get_num_simulations_remaining()
                    if(print_status):
                        self.print_progress(total_runs,num_remaining)

                    if(num_remaining == 0):
                        if(print_status):
                            print("Simulations Complete")
                        break
                    else:
                        time.sleep(0.5)
            except (KeyboardInterrupt, SystemExit):
                print("Shutting down...")
                sys.exit(1)

    def print_progress(self,total_sims,sims_remaining):
        sims_remaining = self.simulations_remaining
        os.system('clear')   
        print("Simulation progress: %d%% " % ((total_sims-sims_remaining)*100.0/total_sims))
        print("%d of %d remaining"%(sims_remaining,total_sims))
        print("\n-------------------------------------------")
        print("Currently Running Simulations")
        print("-------------------------------------------")
        print("Id \t EbN0 (dB) \t Errors \t Modulation")
        for k,v in self.progress.copy().iteritems():                        
            title = self.__sim_map[k].title if k in self.__sim_map.keys() else "Unknown"
            print("%d \t   %1.3f \t   %d \t\t %s" %(k,v['ebno_db'],v['total_errors'],title))
