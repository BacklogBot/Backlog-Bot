import game    

def printList(l):
    for i in range(len(l)):
        print(l[i].getName() + " with " + str(l[i].getInterest()) ) 

def get_pivot(input_list, starting, ending):  #uses median of three method!
    middle = (starting+ending)//2  #get the average of the starting and ending indices
    pivot = ending

    #do a bunch of comparisons to choose the median item from starting, ending, and middle
    if input_list[starting].getInterest() < input_list[middle].getInterest():
        #if here, we already know starting < middle
        if input_list[middle].getInterest() < input_list[ending].getInterest():
            #starting < middle < ending
            pivot = middle
    elif input_list[starting].getInterest() < input_list[ending].getInterest():  
        #if here, we already know middle < starting and now we have starting < ending...middle < starting < ending
        pivot = starting
    #if we end up never reassigning pivot, we know the middle and starting are not the median which leaves ending as the only possibility
    return pivot

def compare(game1, game2):
    '''
    basically, we consider interest to have a higher weight than time played, while do our comparisons

    weight really comes into play when their needs to be tie-breakers
    '''
    if game1.getInterest() > game2.getInterest():
        return 1
    elif game1.getInterest() < game2.getInterest():
        return -1    
    else:
        if game1.getTimePlayde() > game2.getTimePlayde():
            return 1
        elif game1.getTimePlayde() < game2.getTimePlayde():
            return -1
        else:
            return 0       

def partition(input_list, starting, ending):
    pivot_index = get_pivot(input_list, starting, ending) #get the item we'll compare everything else to
    pivot_value = input_list[pivot_index]
    
    #move the pivot item into the leftmost position
    input_list[pivot_index] = input_list[starting]
    input_list[starting] = pivot_value

    border = starting
    for i in range(starting, ending+1): 
        if ( compare(input_list[i], input_list[starting]) == 1 ):
            border += 1 

            #swap the current item with the border item
            temp = input_list[i]
            input_list[i] = input_list[border]
            input_list[border] = temp
            #this ensures all items less than the pivot will be moved to the LHS of the list

    #after going through the whole list, swap the starting (which is now the pivot) and the border
    temp = input_list[starting]
    input_list[starting] = input_list[border]
    input_list[border] = temp

    return border 

def quicksort(input_list, starting, ending):
    #if there's more than 1 item to be sorted   
    if starting < ending: 
        pivot = partition(input_list, starting, ending)
        quicksort(input_list, starting, pivot-1)  #sort all items to the left of pivot
        quicksort(input_list, pivot+1, ending)  #sort all items to the right of pivot

def sortGames(input_list):  #uses quicksort to sort games passed in the list l
    quicksort(input_list, 0, len(l)-1)

if __name__ == "__main__":
    g1 = game.Game("Dishonored", 10, 10, ["Stealth", "RPG"], 10)
    g2 = game.Game("Super Mario Bros", 10, 7, [], 5)
    g3 = game.Game("Halo", 10, 5, [], 7)
    l = [g3,g2,g1]
    old_l = list(l)
    sortGames(l)

    print("\nSTARTING WITH...")
    printList(old_l)


    print("\nENDING WITH...")
    printList(l)    