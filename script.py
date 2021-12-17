from os import write
import os
import json
import re

original = './build/ARM/gem5.opt -d spec_results/speclibm configs/example/se.py --cpu- type=MinorCPU --caches --l2cache --l1d_size=32kB --l1i_size=64kB --l2_size=512kB --l1i_assoc=1 --l1d_assoc=1 --l2_assoc=2 --cacheline_size=64 --cpu-clock=1GHz -c spec_cpu2006/470.lbm/src/speclibm -o "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 \
spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000'

# parameters
commited_insts = "system.cpu.committedInsts"
sim_insts = "sim_insts"
data_cache_replacements = "system.cpu.dcache.replacements"
l2_accesse = "system.l2.tags.data_accesses"  #not 100% sure may be: system.l2.overall_accesses::total



time = "sim_seconds" #xronos ektelesis
cpi = "system.cpu.cpi"
l1inst_missrate = "system.cpu.icache.overall_miss_rate::total"
l1data_missrate = "system.cpu.dcache.overall_miss_rate::total"
l2_missrate = "system.l2.overall_miss_rate::total"


#flags
l1d_assoc = [1,4]#[1,4]#[1,2,4,16]
l1i_assoc = [1,4]#1,4]#[1,2,4,16]
l2_assoc = [1,4,16]#[1,4]#[1,2,4,16]

l1d_size = [32, 64, 128, 256, 384, 448]#[32]#[32, 256]#numbers of test 1[32, 128]#[32, 64, 128, 256, 384, 448]
l1i_size = [32, 64, 128, 256, 384, 448]#[32]#[32, 256]#numbers of test 1[64,256]#[32, 64, 128, 256, 384, 448]
l2_size =[512, 1024, 2048, 4096]#[4096]#numbers of test 1[512, 2048]#[512, 1024, 2048, 4096]

cacheline_size =[32, 64, 128] #[128]#numbers of test 1[32, 128]#[32, 64, 128]



# re.findall("\d+\.\d+", "Current Level: 13.4 db.")

# with open('data.csv','r') as f:
    # lines = f.read().split("\n")




def make_conf_file(filename, bms, pars, outp):
	writes = "[Benchmarks]\n"
	for b in bms:
		writes += f"{b}\n"
	writes += "[Parameters]\n"
	for p in pars:
		writes += f"{p}\n"
	writes += f"[Output]\n{outp}"
	with open(filename, 'w') as f:
		f.write(writes)



# --l1d_size=32kB --l1i_size=64kB --l2_size=512kB --l1i_assoc=1 --l1d_assoc=1 --l2_assoc=2 --cacheline_size=64
def run():

	# #flags
	# l1d_assoc = [2]#[1,4]#[1,2,4,16]
	# l1i_assoc = [2]#1,4]#[1,2,4,16]
	# l2_assoc = [8,16]#[1,4]#[1,2,4,16]

	# l1d_size = [ 128, 256, 384, 448]#[32]#[32, 256]#numbers of test 1[32, 128]#[32, 64, 128, 256, 384, 448]
	# l1i_size = [ 128, 256, 384, 448]#[32]#[32, 256]#numbers of test 1[64,256]#[32, 64, 128, 256, 384, 448]
	# l2_size =[ 512, 4096]#[4096]#numbers of test 1[512, 2048]#[512, 1024, 2048, 4096]

	# cacheline_size =[64] #[128]#numbers of test 1[32, 128]#[32, 64, 128
	# # specbzip benchmark
	# name = "specbzip"
	# for l1ds in l1d_size:
	# 	for l1is in l1i_size:
	# 		for l2s in l2_size:
	# 			for cl in cacheline_size:
	# 				for l1da in l1d_assoc:
	# 					for l1ia in l1i_assoc:
	# 						for l2a in l2_assoc:
	# 							if (l1ds + l1is > 512):
	# 								continue
	# 							filepath =  f"spec_results_p2_{name}/{name}__l1ds_{l1ds}__l1id_{l1is}__l2s_{l2s}__l1da_{l1da}__l1ia_{l1ia}__l2a_{l2a}__cl_{cl}"
	# 							# os.system(f'./build/ARM/gem5.opt -d spec_results_p2/{filepath} configs/example/se.py \
	# 							# 	--cpu-type=MinorCPU --caches --l2cache \
	# 							# 		--l1d_size={l1ds}kB --l1i_size={l1is}kB --l2_size={l2s}kB --l1i_assoc={l1ia} --l1d_assoc={l1da} --l2_assoc={l2a} --cacheline_size={cl}\
	# 							# 		-c spec_cpu2006/401.bzip2/src/specbzip -o\
	# 							# 		"spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000')
	# 							os.system(f'./build/ARM/gem5.opt -d {filepath} configs/example/se.py \
	# 							--cpu-type=MinorCPU --caches --l2cache \
	# 							--l1d_size={l1ds}kB --l1i_size={l1is}kB --l2_size={l2s}kB --l1i_assoc={l1ia} --l1d_assoc={l1da} --l2_assoc={l2a} --cacheline_size={cl}\
	# 							-c spec_cpu2006/401.bzip2/src/specbzip -o\
	# 							"spec_cpu2006/401.bzip2/data/input.program 10" -I 10000000')
	# 							with open(f"{filepath}/stats.txt", 'r') as f:
	# 								lines = f.read().split("\n")
	# 							for l in lines:
	# 								if "system.cpu.cpi" in l:
	# 									cpi = float(re.findall("\d+\.\d+", str(l))[0])
	# 							with open(f"{filepath}/../my_stats.csv", 'a') as my_f:
	# 								# {cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl} ####put this as a header
	# 								my_f.write(f"{cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl}\n")

	# specbzip benchmark
	#flags
	l1d_assoc = [2]#[1,4]#[1,2,4,16]
	l1i_assoc = [4]#1,4]#[1,2,4,16]
	l2_assoc = [8,16]#[1,4]#[1,2,4,16]

	l1d_size = [32, 64, 128]#[32]#[32, 256]#numbers of test 1[32, 128]#[32, 64, 128, 256, 384, 448]
	l1i_size = [ 384, 448]#[32]#[32, 256]#numbers of test 1[64,256]#[32, 64, 128, 256, 384, 448]
	l2_size =[ 2048, 4096]#[4096]#numbers of test 1[512, 2048]#[512, 1024, 2048, 4096]

	cacheline_size =[64, 128] #[128]#numbers of test 1[32, 128]#[32, 64, 128
	name = "specmcf"
	for l1ds in l1d_size:
		for l1is in l1i_size:
			for l2s in l2_size:
				for cl in cacheline_size:
					for l1da in l1d_assoc:
						for l1ia in l1i_assoc:
							for l2a in l2_assoc:
								if (l1ds + l1is > 512):
									continue
								filepath =  f"spec_results_p2_{name}/{name}__l1ds_{l1ds}__l1id_{l1is}__l2s_{l2s}__l1da_{l1da}__l1ia_{l1ia}__l2a_{l2a}__cl_{cl}"
								# os.system(f'./build/ARM/gem5.opt -d spec_results_p2/{filepath} configs/example/se.py \
								# 	--cpu-type=MinorCPU --caches --l2cache \
								# 		--l1d_size={l1ds}kB --l1i_size={l1is}kB --l2_size={l2s}kB --l1i_assoc={l1ia} --l1d_assoc={l1da} --l2_assoc={l2a} --cacheline_size={cl}\
								# 		-c spec_cpu2006/401.bzip2/src/specbzip -o\
								# 		"spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000')
								try:
									os.system(f'./build/ARM/gem5.opt -d {filepath} configs/example/se.py --cpu-type=MinorCPU  --caches --l2cache \
									--l1d_size={l1ds}kB --l1i_size={l1is}kB --l2_size={l2s}kB --l1i_assoc={l1ia} --l1d_assoc={l1da} --l2_assoc={l2a} --cacheline_size={cl}\
									-c spec_cpu2006/429.mcf/src/specmcf \
									-o "spec_cpu2006/429.mcf/data/inp.in" -I 10000000')
									with open(f"{filepath}/stats.txt", 'r') as f:
										lines = f.read().split("\n")
									for l in lines:
										if "system.cpu.cpi" in l:
											cpi = float(re.findall("\d+\.\d+", str(l))[0])
									with open(f"{filepath}/../my_stats.csv", 'a') as my_f:
										# {cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl} ####put this as a header
										my_f.write(f"{cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl}\n")
								except : 
									continue


#flags
	l1d_assoc = [2]#[1,4]#[1,2,4,16]
	l1i_assoc = [2]#1,4]#[1,2,4,16]
	l2_assoc = [8,16]#[1,4]#[1,2,4,16]

	l1d_size = [64, 256]#[32]#[32, 256]#numbers of test 1[32, 128]#[32, 64, 128, 256, 384, 448]
	l1i_size =  [64, 128 ]#[32]#[32, 256]#numbers of test 1[64,256]#[32, 64, 128, 256, 384, 448]
	l2_size =[ 2048, 4096]#[4096]#numbers of test 1[512, 2048]#[512, 1024, 2048, 4096]

	cacheline_size =[64, 128] #[128]#numbers of test 1[32, 128]#[32, 64, 128
	name = "spechmmer"
	for l1ds in l1d_size:
		for l1is in l1i_size:
			for l2s in l2_size:
				for cl in cacheline_size:
					for l1da in l1d_assoc:
						for l1ia in l1i_assoc:
							for l2a in l2_assoc:
								if (l1ds + l1is > 512):
									continue
								try:
									filepath =  f"spec_results_p2_{name}/{name}__l1ds_{l1ds}__l1id_{l1is}__l2s_{l2s}__l1da_{l1da}__l1ia_{l1ia}__l2a_{l2a}__cl_{cl}"
									os.system(f'./build/ARM/gem5.opt -d {filepath} configs/example/se.py --cpu-type=MinorCPU  --caches --l2cache \
									--l1d_size={l1ds}kB --l1i_size={l1is}kB --l2_size={l2s}kB --l1i_assoc={l1ia} --l1d_assoc={l1da} --l2_assoc={l2a} --cacheline_size={cl}\
									-c spec_cpu2006/456.hmmer/src/spechmmer -o\
									"-- fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 10000000')
									with open(f"{filepath}/stats.txt", 'r') as f:
										lines = f.read().split("\n")
									for l in lines:
										if "system.cpu.cpi" in l:
											cpi = float(re.findall("\d+\.\d+", str(l))[0])
									with open(f"{filepath}/../my_stats.csv", 'a') as my_f:
										# {cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl} ####put this as a header
										my_f.write(f"{cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl}\n")
								except:
									continue

	
	#flags
	l1d_assoc = [4]#[1,4]#[1,2,4,16]
	l1i_assoc = [2,4]#1,4]#[1,2,4,16]
	l2_assoc = [8,16]#[1,4]#[1,2,4,16]

	l1d_size = [ 128, 256]#[32]#[32, 256]#numbers of test 1[32, 128]#[32, 64, 128, 256, 384, 448]
	l1i_size = [64, 128, 256]#[32]#[32, 256]#numbers of test 1[64,256]#[32, 64, 128, 256, 384, 448]
	l2_size = [4096]#[4096]#numbers of test 1[512, 2048]#[512, 1024, 2048, 4096]

	cacheline_size =[64, 128] #[128]#numbers of test 1[32, 128]#[32, 64, 128
	name = "specsjeng"
	for l1ds in l1d_size:
		for l1is in l1i_size:
			for l2s in l2_size:
				for cl in cacheline_size:
					for l1da in l1d_assoc:
						for l1ia in l1i_assoc:
							for l2a in l2_assoc:
								if (l1ds + l1is > 512):
									continue
								# if l1ds < 384 or l2s < 2048 or l1da != 4 or l1ia != 4 or l2a != 16 or cacheline_size != 32:
								# 	continue
								try:
									filepath =  f"spec_results_p2_{name}/{name}__l1ds_{l1ds}__l1id_{l1is}__l2s_{l2s}__l1da_{l1da}__l1ia_{l1ia}__l2a_{l2a}__cl_{cl}"
									os.system(f'./build/ARM/gem5.opt -d {filepath} configs/example/se.py --cpu-type=MinorCPU --caches --l2cache \
									--l1d_size={l1ds}kB --l1i_size={l1is}kB --l2_size={l2s}kB --l1i_assoc={l1ia} --l1d_assoc={l1da} --l2_assoc={l2a} --cacheline_size={cl}\
									-c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 10000000')
									with open(f"{filepath}/stats.txt", 'r') as f:
										lines = f.read().split("\n")
									for l in lines:
										if "system.cpu.cpi" in l:
											cpi = float(re.findall("\d+\.\d+", str(l))[0])
									with open(f"{filepath}/../my_stats.csv", 'a') as my_f:
										# {cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl} ####put this as a header
										my_f.write(f"{cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl}\n")
								except:
									continue


#flags
	l1d_assoc = [2]#[1,4]#[1,2,4,16]
	l1i_assoc = [4]#1,4]#[1,2,4,16]
	l2_assoc = [8,16]#[1,4]#[1,2,4,16]

	l1d_size = [128, 256]#[32]#[32, 256]#numbers of test 1[32, 128]#[32, 64, 128, 256, 384, 448]
	l1i_size = [ 64, 128]#[32]#[32, 256]#numbers of test 1[64,256]#[32, 64, 128, 256, 384, 448]
	l2_size =[ 4096]#[4096]#numbers of test 1[512, 2048]#[512, 1024, 2048, 4096]

	cacheline_size =[64, 128] #[128]#numbers of test 1[32, 128]#[32, 64, 128
	name = "speclibm"
	for l1ds in l1d_size:
		for l1is in l1i_size:
			for l2s in l2_size:
				for cl in cacheline_size:
					for l1da in l1d_assoc:
						for l1ia in l1i_assoc:
							for l2a in l2_assoc:
								if (l1ds + l1is > 512):
									continue
								try:
									filepath =  f"spec_results_p2_{name}/{name}__l1ds_{l1ds}__l1id_{l1is}__l2s_{l2s}__l1da_{l1da}__l1ia_{l1ia}__l2a_{l2a}__cl_{cl}"
									os.system(f'./build/ARM/gem5.opt -d {filepath} configs/example/se.py --cpu-type=MinorCPU \
									--caches --l2cache \
									--l1d_size={l1ds}kB --l1i_size={l1is}kB --l2_size={l2s}kB --l1i_assoc={l1ia} --l1d_assoc={l1da} --l2_assoc={l2a} --cacheline_size={cl}\
									-c spec_cpu2006/470.lbm/src/speclibm -o\
									"20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 10000000')
									with open(f"{filepath}/stats.txt", 'r') as f:
										lines = f.read().split("\n")
									for l in lines:
										if "system.cpu.cpi" in l:
											cpi = float(re.findall("\d+\.\d+", str(l))[0])
									with open(f"{filepath}/../my_stats.csv", 'a') as my_f:
										# {cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl} ####put this as a header
										my_f.write(f"{cpi},{l1ds},{l1is},{l2s},{l1da},{l1ia},{l2a},{cl}\n")
								except:
									continue


							


	


def run_part1():
	os.system('./build/ARM/gem5.opt -d spec_results/1_5_specbzip configs/example/se.py \
		--cpu-type=MinorCPU --cpu-clock=1.5GHz --caches --l2cache -c spec_cpu2006/401.bzip2/src/specbzip -o\
			 "spec_cpu2006/401.bzip2/data/input.program 10" -I 100000000')
	os.system('./build/ARM/gem5.opt -d spec_results/1_5_specmcf configs/example/se.py \
		--cpu-type=MinorCPU --cpu-clock=1.5GHz --caches --l2cache -c spec_cpu2006/429.mcf/src/specmcf\
			 -o "spec_cpu2006/429.mcf/data/inp.in" -I 100000000')
	os.system('./build/ARM/gem5.opt -d spec_results/1_5_spechmmer configs/example/se.py --cpu-\
		type=MinorCPU --cpu-clock=1.5GHz --caches --l2cache -c spec_cpu2006/456.hmmer/src/spechmmer -o\
		 "-- fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 spec_cpu2006/456.hmmer/data/bombesin.hmm" -I 100000000')
	os.system('./build/ARM/gem5.opt -d spec_results/1_5_specsjeng configs/example/se.py --cpu-type=MinorCPU --cpu-clock=1.5GHz --caches \
		--l2cache -c spec_cpu2006/458.sjeng/src/specsjeng -o "spec_cpu2006/458.sjeng/data/test.txt" -I 100000000')
	os.system('./build/ARM/gem5.opt -d spec_results/1_5_speclibm configs/example/se.py --cpu-type=MinorCPU --cpu-clock=1.5GHz \
		--caches --l2cache -c spec_cpu2006/470.lbm/src/speclibm -o\
		 "20 spec_cpu2006/470.lbm/data/lbm.in 0 1 spec_cpu2006/470.lbm/data/100_100_130_cf_a.of" -I 100000000')