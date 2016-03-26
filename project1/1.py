def fizzbuzz(intList):
    '''
    Your fizzbuzz function. The grader will run `fizzbuzz(intList)` to check if your
    function returns the correct output.
    
    intList: list containing integers

    Make sure you write the script so that your algorithm is part of the
    function; you do not need to call the function yourself.
    '''
    www=list(intList)
    for n,i in enumerate(www):
        if i%3==0:
            www[n]="Fizz"
        if i%5==0:
            www[n]="Buzz"
        if i%3==0 and i%5 ==0:
            www[n]="FizzBuzz"
    return www
            
        