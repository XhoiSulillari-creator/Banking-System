from customer_repository import CustomerRepository
from account_repository import AccountRepository
from transaction import Transaction
from authentication import AuthenticationService


class Bank:
    def __init__(
        self,
        name,
        customer_repository,
        account_repository,
        authentication_service
    ):
        self.name = name
        self.customer_repository = customer_repository
        self.account_repository = account_repository
        self.authentication_service = authentication_service

    def add_customer(self, customer):
        existing_customer = self.customer_repository.load(
            customer.customer_id
        )

        if existing_customer is not None:
            return False

        self.customer_repository.save(customer)
        return True

    def get_customer(self, customer_id):
        return self.customer_repository.load(customer_id)

    def add_account(self, account):
        customer = self.customer_repository.load(
            account.owner.customer_id
        )

        if customer is None:
            return False

        existing_account = self.account_repository.load(
            account.account_id
        )

        if existing_account is not None:
            return False

        self.account_repository.save(account)
        return True

    def get_account(self, account_id):
        return self.account_repository.load(account_id)

    def transfer(
        self,
        transaction_id,
        source_account_id,
        destination_account_id,
        amount
    ):
        source_account = self.get_account(source_account_id)
        destination_account = self.get_account(destination_account_id)

        if source_account is None or destination_account is None:
            return False

        transaction = Transaction(
            transaction_id,
            source_account,
            destination_account,
            amount
        )

        success = transaction.execute()

        if not success:
            return False

        self.account_repository.save(source_account)
        self.account_repository.save(destination_account)

        return True

    def register_customer_credentials(self, customer_id, password):
        customer = self.get_customer(customer_id)

        if customer is None:
            return False

        self.authentication_service.register(
            customer_id,
            password
        )

        return True

    def authenticate_customer(self, customer_id, password):
        return self.authentication_service.authenticate(
            customer_id,
            password
    )