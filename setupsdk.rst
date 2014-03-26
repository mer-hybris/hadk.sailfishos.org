Preparing the Mer SDK
---------------------


You'll need some tools which are not installed into the Mer SDK by default:


.. code-block:: console

  MER_SDK$

  sudo zypper in createrepo zip

createrepo is needed to build repos if you want/need to update local targets

zip is needed to create the final installer
