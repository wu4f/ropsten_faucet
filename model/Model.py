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

    def insert(self, email, ip, wallet):
        """
        Inserts entry into database
        :param email: String
        :param ip: String
        :param wallet: String
        :return: none
        """
        pass

    def update(self, email, ip, wallet):
        """
        Updates entry in database
        :param email: String
        :param ip: String
        :param wallet: String
        :return: none
        """
        pass
