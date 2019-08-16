NAME    := libfabric
SRC_EXT := gz
SOURCE   = https://github.com/ofiwg/$(NAME)/archive/v$(VERSION).tar.$(SRC_EXT)

include packaging/Makefile_packaging.mk
