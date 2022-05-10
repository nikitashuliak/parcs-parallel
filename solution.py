from Pyro4 import expose
import time


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        arr = self.read_input()
        start_time = time.time()
        step = len(arr) / len(self.workers)

        # map
        mapped = []
        for i in range(0, len(self.workers)):
            if (i+1 == len(self.workers)):
                mapped.append(self.workers[i].mymap(arr, i * step, len(arr)))
            else:
                mapped.append(self.workers[i].mymap(arr, i * step,
                                                    i * step + step))

        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))
        result = reduced[0]
        for i in range(1, len(reduced)):
            result = Solver.lcm(result, reduced[i])
        # output
        elapsed_time = time.time() - start_time
        output = Solver.create_output(result, elapsed_time, len(self.workers))
        # for i in reduced:
        #     output = output + str(i) + " "
        self.write_output(output)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(arr, a, b):
        res = arr[a]
        for i in range(a+1, b, 1):
            res = Solver.lcm(res, arr[i])
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = []
        for x in mapped:
            output.append(x.value)
        return output

    @staticmethod
    def lcm(num1, num2):
        if(num1 > num2):
            num = num1
            den = num2
        else:
            num = num2
            den = num1
        rem = num % den
        while(rem != 0):
            num = den
            den = rem
            rem = num % den
        gcd = den
        lcm = int(int(num1 * num2)/int(gcd))
        return lcm

    @staticmethod
    def create_output(result, elapsed_time, num_of_workers):
        return \
            "LCM of an array is : " + str(result) + "\n" + \
            "Time spent : " + str(elapsed_time) + "\n" + \
            "Number of workers: " + str(num_of_workers) + "\n"

    def read_input(self):
        f = open(self.input_file_name, 'r')
        arr = f.read()
        nums = arr.split(' ')
        res = map(int, nums)
        f.close()
        return list(res)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
