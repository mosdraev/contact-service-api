from ...models.contact import Contact
from sqlalchemy.exc import IntegrityError


class ContactOperations:
    def __init__(self, db):
        self.db = db

    def get_contacts(self, owner_id):
        contacts = self.db.query(Contact).filter(Contact.owner_id == owner_id).all()
        return {"contacts": contacts}

    def get_contact(self, owner_id, contact_id):
        contact = self.db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
        return contact

    def create_contact(self, data, owner_id):
        data.owner_id = owner_id
        new_contact = Contact(**data.dict())

        try:
            self.db.add(new_contact)
            self.db.commit()
            self.db.refresh(new_contact)

            return new_contact
        except IntegrityError as e:
            return False

    def update_contact(self, data, contact_id, owner_id):
        find_contact = self.db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id)

        if find_contact.first():
            data = ContactOperations.remove_none_values(data.dict())
            find_contact.update(data)
            self.db.commit()

            return find_contact.first()
        return False

    def delete_contact(self, contact_id, owner_id):
        contact = self.get_contact(owner_id, contact_id)
        if contact:
            self.db.delete(contact)
            self.db.commit()

            return True
        return False

    @classmethod
    def remove_none_values(cls, dictionary_data):
        for item in list(dictionary_data):
            if dictionary_data[item] is None:
                dictionary_data.pop(item)
        return dictionary_data
