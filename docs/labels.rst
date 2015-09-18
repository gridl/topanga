Label Specification
###################
Since the goal of Topanga is to be able to manage groups of containers in an application apart from the command line
or a file, we need to be able to inspect a group of running containers and get back to original config.

Initial Labels::

  topanga.app.name
  topanga.app.application_name
  topanga.app.links
  topanga.app.volumes_from

For links and volumes_from it will have a JSON string of the structure::

  {
    logical: [<names>],
    current: [<container_ids>]
  }

