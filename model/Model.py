class Model():
    def select(self, email, ip, wallet):
        """
        Gets last time ETH received for email, ip, or wallet
        :param email: String
        :param ip: String
        :param wallet: String
        :return: Integer seconds
        """
        pass
    
    def select_all(self):
        """
        Gets all rows from the database
        :return: Rows of database
        """
        pass

    def select_last_ip(self, number):
        """
        Gets recent requests from the database
        :param: number of requests
        :return: List of /16 IP prefixes for previous number of requests
        """
        pass

    def insert(self, email, ip, wallet, eth):
        """
        Inserts entry into database
        :param email: String
        :param ip: String
        :param wallet: String
        :param eth: Real
        :return: True
        :raises: Database errors on connection and insertion
        """
        pass

    def update(self, email, ip, wallet, eth):
        """
        Updates entry in database
        :param email: String
        :param ip: String
        :param wallet: String
        :param eth: Real
        :return: True
        :raises: Database errors on connection and insertion
        """
        pass
