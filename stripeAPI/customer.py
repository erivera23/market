from . import stripe

def create_customer(user):
    customer = stripe.Customer.create(
        description=user.descripcion
    )

    return customer