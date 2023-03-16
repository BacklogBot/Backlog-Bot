def get_pivot(input_list, starting, ending):  #uses median of three method!
    middle = (starting+ending)//2  #get the average of the starting and ending indices
    pivot = ending

    #do a bunch of comparisons to choose the median item from starting, ending, and middle
    if input_list[starting] < input_list[middle]:
        #if here, we already know starting < middle
        if input_list[middle] < input_list[ending]:
            #starting < middle < ending
            pivot = middle
    elif input_list[starting] < input_list[ending]:  
        #if here, we already know middle < starting and now we have starting < ending...middle < starting < ending
        pivot = starting
    #if we end up never reassigning pivot, we know the middle and starting are not the median which leaves ending as the only possibility
    return pivot

def partition(input_list, starting, ending):
    pivot_index = get_pivot(input_list, starting, ending) #get the item we'll compare everything else to
    pivot_value = input_list[pivot_index]
    
    #move the pivot item into the leftmost position
    input_list[pivot_index] = input_list[starting]
    input_list[starting] = pivot_value

    border = starting
    for i in range(starting, ending+1): #iterate through all items in the list
        if input_list[i] < pivot_value:
            #border is how we physically distinguish which items are < pivot and which are > the pivot
            #move the border along the list as we push "< pivot" items behind it
            border += 1 #now that we've compared the current item, increment the border item to reflect this update

            #swap the current item with the border item
            input_list[i] = temp
            input_list[i] = input_list[border]
            input_list[border] = temp
            #this ensures all items less than the pivot will be moved to the LHS of the list
    
    #basically, the border was acting as the proxy for the pivot, seeking its proper position within the list. 
    #now that we have found it, we can move the pivot to this position

    #after going through the whole list, swap the starting (which is now the pivot) and the border
    input_list[starting] = temp
    input_list[starting] = input_list[border]
    input_list[border] = temp

    #the border now represents the proper (so correct index in a sorted list) pivot point, so return it
    return border 

def quicksort(input_list, starting, ending):
    #if there's more than 1 item to be sorted    
    if starting < ending: 
        pivot = partition(input_list, starting, ending)
        quicksort(input_list, starting, pivot-1)  #sort all items to the left of pivot
        quicksort(input_list, pivot+1, ending)  #sort all items to the right of pivot

def sortGames(input_list):  #uses quicksort to sort games passed in the list l
    quicksort(input_list, 0, len(l)-1)
