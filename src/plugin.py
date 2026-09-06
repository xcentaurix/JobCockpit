# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


from Plugins.Plugin import PluginDescriptor
from .Debug import logger
from .Version import PLUGIN, VERSION
from .JobCockpit import JobCockpit
from .PluginUtils import WHERE_JOBCOCKPIT
from . import _
from .JobSupervisor import JobSupervisor
from .SkinUtils import loadPluginSkin


loadPluginSkin(PLUGIN)


def main(session, plugin_id="", **__kwargs):
    logger.info("plugin_id: %s", plugin_id)
    session.open(JobCockpit, plugin_id)


def autoStart(reason, **kwargs):
    if reason == 0:  # startup
        if "session" in kwargs:
            logger.info("+++ Version: %s starts...", VERSION)
            JobSupervisor.getInstance()
    elif reason == 1:  # shutdown
        logger.info("--- shutdown")


def Plugins(**__kwargs):
    descriptors = [
        PluginDescriptor(
            where=[
                PluginDescriptor.WHERE_AUTOSTART,
                PluginDescriptor.WHERE_SESSIONSTART
            ],
            fnc=autoStart,
            needsRestart=True
        ),
        PluginDescriptor(
            name="JobCockpit",
            where=[
                PluginDescriptor.WHERE_PLUGINMENU,
                PluginDescriptor.WHERE_EXTENSIONSMENU
            ],
            icon="JobCockpit.png",
            description=_("Manage Jobs"),
            fnc=main,
            needsRestart=True
        ),
        PluginDescriptor(
            name=_("Jobs"),
            description=_("Manage Jobs"),
            where=WHERE_JOBCOCKPIT,
            fnc=main,
            needsRestart=True
        ),
    ]
    try:
        descriptors += [
            PluginDescriptor(
                where=PluginDescriptor.WHERE_SKINCHANGE,
                fnc=loadPluginSkin
            )
        ]
    except Exception:
        pass

    return descriptors
