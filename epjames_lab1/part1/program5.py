class FindPair:
    def __init__(self, numbers):
        self.numbers = numbers
    
    def find_pair(self, target):
        # Create dictionary to store index as key and number as value
        num_dict = {}
        
        for index, number in enumerate(self.numbers):
            # Calculate the complement 
            complement = target - number
            #print(complement)
            # Check if the complement exists in the dictionary
            if complement in num_dict:
                return num_dict[complement], index
            
            # Store the current number with its index in the dictionary
            num_dict[number] = index
        
        # If no pair is found
        return None

#Numbers given
numbers = [10, 20, 10, 40, 50, 60, 70]

# Create an instance of PairFinder
finder = FindPair(numbers)
# Ask the user for the target number
target = int(input("What is your target number? "))

# Find and print the indices of the pair whose sum equals the target number
result = finder.find_pair(target)
#print(result)
if result:
    index1, index2 = result
    print(f"index1={index1}, index2={index2}")
else:
    print("No pair found that sums to the target number.")
