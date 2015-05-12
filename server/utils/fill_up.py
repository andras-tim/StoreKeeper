#!../flask/bin/python
"""
Fill up database with huge amount of test data
"""
import json
import os.path
import random
import sys
from sqlalchemy.exc import IntegrityError

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir, '..'))
base_record_count_per_table = 1000

from app.server import db
from app.models import Unit, Vendor, Item, User, UserConfig, Customer, Barcode, Work, WorkItem, Acquisition, \
    AcquisitionItem, Stocktaking, StocktakingItem


def get_data() -> dict:
    with open(os.path.join(basedir, 'fill_up.json'), 'r') as fd:
        data = json.load(fd)
        fd.close()
    return data


def get_count(base_multiplier: float=1) -> int:
    multiplier = base_multiplier * (random.randint(7, 11) / 10)
    return int(base_record_count_per_table * multiplier)


def iterate_acquisitions(data: dict):
    for i in range(get_count()):
        comment = ''
        if random.randint(1, 10) == 1:
            comment = random.choice(data['comments'])
        yield Acquisition(
            comment=comment
        )


def iterate_acquisition_items(data: dict):
    acquisition_count = Acquisition.query.count()
    acquisition_ids = list(range(1, acquisition_count + 1))
    random.shuffle(acquisition_ids)

    item_count = Item.query.count()
    item_ids = list(range(1, item_count + 1))

    for acquisition_id in acquisition_ids:
        for i in range(random.randint(1, 2)):  # TODO: INCREASE
            yield AcquisitionItem(
                acquisition_id=acquisition_id,
                item_id=random.choice(item_ids),  # TODO: UNIQUE
                quantity=random.randint(1, 20)
            )


def iterate_barcodes(data: dict):
    item_count = Item.query.count()
    item_ids = list(range(1, item_count + 1))
    random.shuffle(item_ids)

    for item_id in item_ids:
        yield Barcode(
            barcode='SK{number}'.format(
                number=random.randint(100000, 999999)
            ),
            quantity=1,
            item_id=item_id,
            main=True
        )
        for i in range(random.randint(0, 2)):
            yield Barcode(
                barcode='SK{number}'.format(
                    number=random.randint(100000, 999999)
                ),
                quantity=random.randint(1, 10) * 5,
                item_id=item_id,
                main=False
            )


def iterate_customers(data: dict):
    for i in range(get_count()):
        yield Customer(
            name='{adj} {noun} {ent}'.format(  # TODO: UNIQUE
                adj=random.choice(data['nouns']),
                noun=random.choice(data['nouns']),
                ent=random.choice(data['business_entities'])
            ).title()
        )


def iterate_items(data: dict):
    vendor_count = Vendor.query.count()
    unit_count = Unit.query.count()

    for i in range(get_count(3)):
        yield Item(
            name='{adj1} {adj2} {item}'.format(  # TODO: UNIQUE
                adj1=random.choice(data['nouns']),
                adj2=random.choice(data['nouns']),
                item=random.choice(data['items'])
            ).capitalize(),
            vendor_id=random.randrange(vendor_count) + 1,
            article_number=random.randint(1000, 999999),
            quantity=random.randint(0, 1000),
            unit_id=random.randrange(unit_count) + 1
        )


def iterate_stocktakings(data: dict):
    for i in range(get_count()):
        comment = ''
        if random.randint(1, 10) == 1:
            comment = random.choice(data['comments'])
        yield Stocktaking(
            comment=comment
        )


def iterate_stocktaking_items(data: dict):
    stocktaking_count = Stocktaking.query.count()
    stocktaking_ids = list(range(1, stocktaking_count + 1))
    random.shuffle(stocktaking_ids)

    item_count = Item.query.count()
    item_ids = list(range(1, item_count + 1))

    for stocktaking_id in stocktaking_ids:
        for i in range(random.randint(1, 2)):  # TODO: INCREASE
            yield StocktakingItem(
                stocktaking_id=stocktaking_id,
                item_id=random.choice(item_ids),  # TODO: UNIQUE
                quantity=random.randint(0, 20)
            )


def iterate_units(data: dict):
    for unit in data['units'][:get_count()]:
        yield Unit(unit=unit)


def iterate_users(data: dict):
    usernames = list(data['usernames'])

    for i in range(min(get_count(0.5), len(usernames))):
        username = random.choice(usernames)
        usernames.remove(username)

        user = User(
            username=username,
            email='{username}@{domain}.{country}'.format(
                username=username,
                domain=random.choice(data['nouns']),
                country=random.choice(data['countries'])
            ),
            admin=(random.randint(1, 100) == 1),
            disabled=(random.randint(1, 1000) == 1),
            password_hash="$" + hex(random.randint(1, 1000))
        )
        # user.set_password(hex(random.randint(1, 1000)))
        yield user


def iterate_user_config(data: dict):
    user_count = User.query.count()
    user_ids = list(range(1, user_count + 1))
    random.shuffle(user_ids)

    for user_id in user_ids:
        yield UserConfig(
            user_id=user_id,
            name="lang",
            value=random.choice(data['countries'])
        )


def iterate_vendors(data: dict):
    for i in range(get_count()):
        yield Vendor(
            name='{adj} {noun} {ent}'.format(  # TODO: UNIQUE
                adj=random.choice(data['nouns']),
                noun=random.choice(data['nouns']),
                ent=random.choice(data['business_entities'])
            ).title()
        )


def iterate_works(data: dict):
    customer_count = Customer.query.count()
    customer_ids = list(range(1, customer_count + 1))

    for i in range(get_count()):
        comment = ''
        if random.randint(1, 10) == 1:
            comment = random.choice(data['comments'])
        yield Work(
            customer_id=random.choice(customer_ids),
            comment=comment
        )


def iterate_work_items(data: dict):
    work_count = Work.query.count()
    work_ids = list(range(1, work_count + 1))
    random.shuffle(work_ids)

    item_count = Item.query.count()
    item_ids = list(range(1, item_count + 1))

    for work_id in work_ids:
        for i in range(random.randint(1, 2)):  # TODO: INCREASE
            yield WorkItem(
                work_id=work_id,
                item_id=random.choice(item_ids),  # TODO: UNIQUE
                outbound_quantity=random.randint(1, 20),
                returned_quantity=random.randint(0, 3) * 6
            )


def main():
    commit_batch_size = 200
    iterators = [
        iterate_users,
        iterate_user_config,
        iterate_vendors,
        iterate_units,
        iterate_customers,
        iterate_items,
        iterate_barcodes,
        iterate_works,
        iterate_work_items,
        iterate_acquisitions,
        iterate_acquisition_items,
        iterate_stocktakings,
        iterate_stocktaking_items,
    ]
    data = get_data()

    for object_iterator in iterators:
        name = object_iterator.__name__.replace('iterate_', '').replace('_', ' ')
        sys.stdout.write(' * Generating {}...'.format(name))
        sys.stdout.flush()

        iterator = object_iterator(data)
        commited_rows = 0
        while True:
            record_in_batch = 0

            for new_object in iterator:
                db.session.add(new_object)
                record_in_batch += 1
                if record_in_batch == commit_batch_size:
                    break

            if record_in_batch == 0:
                print(' Done [{}]'.format(commited_rows))
                break

            try:
                db.session.commit()
                commited_rows += record_in_batch
                sys.stdout.write('.')
            except IntegrityError:  # TODO: Fix unicity TODOs above
                sys.stdout.write('s')
                db.session.rollback()
            sys.stdout.flush()

    print('All done')

if __name__ == '__main__':
    sys.exit(main())
