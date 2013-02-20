from plone.testing import z2

from plone.app.testing import *
import plomino.easynewsletter

FIXTURE = PloneWithPackageLayer(zcml_filename="configure.zcml",
                                zcml_package=plomino.easynewsletter,
                                additional_z2_products=[],
                                gs_profile_id='plomino.easynewsletter:default',
                                name="plomino.easynewsletter:FIXTURE")

INTEGRATION = IntegrationTesting(bases=(FIXTURE,),
                        name="plomino.easynewsletter:Integration")

FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,),
                        name="plomino.easynewsletter:Functional")

