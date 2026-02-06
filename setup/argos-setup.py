import argostranslate.package
import argostranslate.translate


def download(from_code, to_code) :

    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())

    # Translate
    #translatedText = argostranslate.translate.translate("Hello World", from_code, to_code)
    #print(translatedText)
    # '¡Hola Mundo!'

    return


from_code = "en"
to_code = "es"
download(to_code, from_code)
download(from_code, to_code)