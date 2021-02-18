from threading import Thread
from time import sleep


class Consumer(Thread):
    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a consumer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.name = kwargs['name']

    def run(self):
        # iterate through all client carts
        for cart in self.carts:
            # get each card id
            cart_id = self.marketplace.new_cart()
            # iterate through the actions in each cart
            for action in cart:
                # execute the action a number of 'quantity' times
                for _ in range(action['quantity']):
                    if action['type'] == 'add':
                        while not self.marketplace.add_to_cart(cart_id, action['product']):
                            # wait and retry to add the product till success
                            sleep(self.retry_wait_time)
                    else:
                        # remove product from cart and add it to the list where it was taken from
                        self.marketplace.remove_from_cart(cart_id, action['product'])
            order = self.marketplace.place_order(cart_id)
            # reverse the list to keep the chronological order
            order = reversed(order)
            for product in order:
                print(self.name + " bought " + str(product[1]))
