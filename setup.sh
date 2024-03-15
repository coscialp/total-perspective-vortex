#!/usr/bin/env bash

function _check-pyenv-version-name {
    version_name="$(pyenv version-name)"
    if [ "$version_name" = "venv-tpv-3.8" ]; then
      return 0
    else
      return 1
    fi
}

function setup_venv {
  python3 -m venv venv
  source venv/bin/activate
}

function setup_pyenv {
    if pyenv -v; then
        echo "pyenv is already installed"
    else
        echo "pyenv is not installed"
        echo "Installing pyenv"
        curl https://pyenv.run | bash
        export PYENV_ROOT="$HOME/.pyenv"
        [[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init -)"
    fi

    if pyenv install --list | grep -Fq " 3.8.10"; then
        echo "Python 3.8.10 is already installed"
    else
        echo "Python 3.8.10 is not installed"
        echo "Installing Python 3.8.10"
        pyenv install 3.8.10
    fi

    if pyenv virtualenvs | grep -Fq "3.8.10/envs/venv-tpv-3.8"; then
        echo "Python 3.8.10 venv-tpv-3.8 is already installed"
    else
        echo "Python 3.8.10 venv-tpv-3.8 is not installed"
        echo "Installing Python 3.8.10 venv-tpv-3.8"
        pyenv virtualenv 3.8.10 venv-tpv-3.8
    fi

    if _check-pyenv-version-name; then
        echo "venv-tpv-3.8 is already activated"
    else
        echo "venv-tpv-3.8 is not activated"
        echo "Activating venv-tpv-3.8"
        pyenv activate venv-tpv-3.8
    fi
}

function clean {
  if _check-pyenv-version-name; then
    echo "Deactivating venv-tpv-3.8"
    pyenv deactivate
  else
    echo "venv-tpv-3.8 is not activated"
  fi
}

function fclean {
    clean
    if pyenv virtualenvs | grep -Fq "3.8.10/envs/venv-tpv-3.8"; then
        echo "Deleting Python 3.8.10 venv-tpv-3.8"
        pyenv virtualenv-delete -f 3.8.10/envs/venv-tpv-3.8
    else
        echo "Python 3.8.10 venv-tpv-3.8 is not installed"
    fi
}

function install_requirements {
  version_name="$(pyenv version-name)"
  if [ -f "requirements.txt" ] && [ "$version_name" = "venv-tpv-3.8" ]; then
    echo "Installing requirements"
    pip install -r requirements.txt
  else
    echo "requirements.txt not found"
  fi
}

function help {
  echo "Usage: source ./setup.sh {install|clean|fclean|install-requirements|pip-install <package>}"
  echo "Warning: This script works only with source command"
  echo
  echo "Commands:"
  echo "  \`install\`: Install pyenv, Python 3.8.10, venv-tpv-3.8 and requirements"
  echo "  \`clean\`: Deactivate venv-tpv-3.8"
  echo "  \`fclean\`: Deactivate venv-tpv-3.8 and delete venv-tpv-3.8"
  echo "  \`install-requirements\`: Install requirements"
  echo "  \`pip-install <package>\`: Install a package and update requirements.txt"
}

for arg in "$@"; do
  if [ "$arg" = "-h" ] || [ "$arg" = "--help" ]; then
    help
    return 0
  fi
done

echo "Warning: This script works only with source command"

case $1 in
    "install")
        clean
        setup_venv
#        setup_pyenv
        install_requirements
        ;;

      "clean")
        clean
        ;;

      "fclean")
        fclean
        ;;

      "re")
        fclean
        setup_pyenv
        install_requirements
        ;;

      "install-requirements")
        install_requirements
        ;;

      "pip-install")
      if [ -n "$2" ]; then
        pip install "$2"
        pip freeze > requirements.txt
      else
        echo "Usage: source ./setup.sh pip-install <package>"
      fi
        ;;

      *)
        help
        return 1
        ;;
esac