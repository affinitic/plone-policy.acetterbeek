from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class PolicyAcetterbeek(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import policy.acetterbeek
        xmlconfig.file('configure.zcml',
                       policy.acetterbeek,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'policy.acetterbeek:default')

POLICY_ACETTERBEEK_FIXTURE = PolicyAcetterbeek()
POLICY_ACETTERBEEK_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(POLICY_ACETTERBEEK_FIXTURE, ),
                       name="PolicyAcetterbeek:Integration")