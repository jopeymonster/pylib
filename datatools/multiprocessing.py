# multi-processing

# function - using standard MAP
import multiprocessing

def worker(number):
    return number * number

def main(numbers):
    # Determine the number of processes to use
    num_processes = multiprocessing.cpu_count()
    
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Map the worker function to the numbers list
        results = pool.map(worker, numbers)
    
    # Print results
    print(results)

if __name__ == "__main__":
    numbers = list(range(1, 10001))  # Adjust the range as needed
    main(numbers)


# using STARMAP

def worker(arg1, arg2):
    return arg1 * arg2

def main(data):
    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(worker, data)
    print(results)

if __name__ == "__main__":
    data = [(i, i+1) for i in range(1, 10001)]  # Adjust the data as needed
    main(data)


# use case
import multiprocessing

def worker(number, result_queue):
    result = number * number
    result_queue.put(result)

def main(numbers):
    processes = []
    result_queue = multiprocessing.Queue()
    
    # Create and start processes
    for number in numbers:
        process = multiprocessing.Process(target=worker, args=(number, result_queue))
        processes.append(process)
        process.start()
    
    # Wait for all processes to finish
    for process in processes:
        process.join()
    
    # Retrieve results
    results = [result_queue.get() for _ in numbers]
    print(results)

if __name__ == "__main__":
    numbers = list(range(1, 10001))  # Adjust the range as needed
    main(numbers)
