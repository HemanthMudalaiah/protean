import pytest

from protean.core.subscriber import BaseSubscriber
from protean.exceptions import NotSupportedError
from protean.utils import fully_qualified_name


class NotifySSOSubscriber(BaseSubscriber):
    """Subscriber that notifies an external SSO system
    that a new person was added into the system
    """

    def notify(self, data: dict):
        print("Received data: ", data)


class TestSubscriberInitialization:
    def test_that_base_subscriber_class_cannot_be_instantiated(self):
        with pytest.raises(NotSupportedError):
            BaseSubscriber()

    def test_that_subscriber_can_be_instantiated(self, test_domain):
        subscriber = NotifySSOSubscriber()
        assert subscriber is not None


class TestSubscriberRegistration:
    def test_that_domain_event_can_be_registered_with_domain(self, test_domain):
        test_domain.register(NotifySSOSubscriber, stream="person_added")

        assert (
            fully_qualified_name(NotifySSOSubscriber)
            in test_domain.registry.subscribers
        )

    def test_that_domain_event_can_be_registered_via_annotations(self, test_domain):
        @test_domain.subscriber(stream="person_added")
        class AnnotatedSubscriber:
            def special_method(self):
                pass

        assert (
            fully_qualified_name(AnnotatedSubscriber)
            in test_domain.registry.subscribers
        )
