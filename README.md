# Python Producer-Consumer

Classic multithreading problem, implemented in python, using 3 classes:

### a. Producer
The producers run as long as there is at least one consumer running, beacuse 
they are daemon threads. They try to publish items in the marketplace.
### b. Consumer
Iterates through the shopiing carts and executes an action (adds or removes a 
product).
### c. Marketplace 
The marketplace is a buffer used by the threads, which provides methods for
adding or removing products, carts, publishing or placing orders. Since it is 
accessed by threads, there are locks in the critical zones