def upgrade(name, callback, end_time):
    {name: 'Some Upgrade', callback: 'function', end_time: 10}
    #Everytime you run the main loop, call a function to compare the current time with the end time, if its past the time, call the callback function