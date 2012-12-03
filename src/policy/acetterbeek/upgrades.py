import logging
from Products.CMFCore.utils import getToolByName
from zope.site.hooks import getSite


def cleanjscss(context):
    """ upgrade steps etterbeek """
    log = logging.getLogger("Policy Etterbeek upgrade step")
    #portal_migration = getToolByName(context, 'portal_migration')
    #portal_migration.upgrade()
    #log.info("Ran Plone Upgrade")
    registry = context.getImportStepRegistry()
    old_steps = ["quintagroup.plonecomments.install",
            "quintagroup.plonecomments.uninstall",
            "collective.plonetruegallery",
            "flashmovie-mimetypesregistry",
            "register-mime-type",
            "quintagroup.captcha.core-various",
            "collective.collage.easyslider.various",
            "quintagroup.captcha.core_uninstall",
            "install-fss",
            "remove-dDuplicate-actions-in-types",
            "remove-duplicate-actions-in-types",
            "register-content-type"]
    for old_step in old_steps:
        if old_step in registry.listSteps():
            registry.unregisterStep(old_step)
            # Unfortunately we manually have to signal the context
            # (portal_setup)
            # that it has changed otherwise this change is not persisted.
            context._p_changed = True
            log.info("Old %s import step removed from import registry.",
                    old_step)
    clean_me = ['IThemeSpecific']
    context.runAllImportStepsFromProfile("profile-policy.acetterbeek:default")

    adapters = getSite().getSiteManager().adapters._adapters
    # 'IThemeSpecific' from module 'acetterbeek.site.browser.interfaces
    for adapter in adapters:
        if adapter.keys():
            if adapter.keys()[0].__module__ == 'zope.interface':
                dic = adapter.values()[0]
                for key in dic.keys():
                    if key.__module__ == 'acetterbeek.site.browser.interfaces':
                        del dic[key]
                        log.info("delete {0} ".format(key.__module__))
                        getSite().getSiteManager().adapters._p_changed = True

    getSite().getSiteManager().adapters._adapters = adapters
    context._p_jar.sync()
    log.info("End upgrade policy etterbeek")
    # OFS.Uninstalled Could not import class 'ATFlashMovie' from module 'Products.ATFlashMovie.ATFlashMovie'
    # WARNING OFS.Uninstalled Could not import class 'Quicklinks' from module 'acetterbeek.site.browser.viewlets'
    # WARNING OFS.Uninstalled Could not import class 'FooterViewlet' from module 'acetterbeek.site.browser.viewlets'
    # WARNING OFS.Uninstalled Could not import class 'LanguageSelector' from module 'acetterbeek.site.browser.viewlets'

