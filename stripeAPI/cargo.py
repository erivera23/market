from . import stripe

def create_cargo(orden):
    if orden.billing_profile and orden.user and orden.user.customer_id:
        cargo = stripe.Charge.create(
            amount = int(orden.total) * 100,
            currency = 'USD',
            description = orden.descripcion,
            customer=orden.user.customer_id,
            source=orden.billing_profile.card_id,
            metadata= {
                'orden_id': orden.id
            }
        )

        return cargo