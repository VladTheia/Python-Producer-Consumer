import threading

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_prod = queue_size_per_producer
        self.stock = {}   # dict of lists for producers (key: String - value: List)
        self.locks = {}   # dict of locks for synchronization (key: String - value: Lock)
        self.carts = []   # list of lists for the shopping carts
        self.prod_id = 1
        self.cart_id = 0 

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        prod_id = "prod" + str(self.prod_id)
        lock = threading.Lock()  # create a lock for each producer
        self.stock[prod_id] = [] # add the producer list
        self.locks[prod_id] = lock # add the producer lock
        self.prod_id += 1  # increment the id for the next producer
        return prod_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        self.locks[producer_id].acquire()  # enter zona thread-safe zone
        if self._producer_not_full(producer_id):  # if the producer list isn't full
            self.stock[producer_id].append(product)  # add the product
            result = True 
        else:
            result = False
        self.locks[producer_id].release()  # exit thread-safe zone
        return result

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        cart_id = self.cart_id
        self.carts.append([])
        self.cart_id += 1
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for key in self.stock:  # iterate through each list of products in the dict
            if product in self.stock[key]:  
                self.locks[key].acquire()  # enter the thread-safe zone
                self.stock[key].remove(product)  # remove from the producer list
                self.carts[cart_id].append((key, product)) # add to the cart
                self.locks[key].release()  # exit thread-safe zone
                return True
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart;
        """
        # iterate through the list of pairs found at the key 'cart_id' in the carts dict
        for pair in self.carts[cart_id]:
            # if the product we want to remove is part of a pair
            if product in pair:
                self.locks[pair[0]].acquire()  # enter thread-safe zone
                self.stock[pair[0]].append(product)  # add to the list it came from
                self.carts[cart_id].remove(pair)  # remove from cart
                self.locks[pair[0]].release()  # exit thread-safe zone
                return True
        return False

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        return self.carts[cart_id]  # return desired cart

    def _producer_not_full(self, prod_id):
        return len(self.stock[prod_id]) < self.queue_size_per_prod
