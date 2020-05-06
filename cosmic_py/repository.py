import abc

import models


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: models.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> models.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(models.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(models.Batch).all()


class FakeRepository(AbstractRepository):
    def __init__(self, batches):
        self.batches = set(batches)

    def add(self, batch):
        self.batches.add(batch)

    def get(self, reference):
        return next(b for b in self.batches if b.reference == reference)

    def list(self):
        return list(self.batches)
