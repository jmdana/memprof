# Maintainer: Jose M. Dana

pkgname=python-memprof
pypiname=memprof
pkgver=0.3.3
pkgrel=1
pkgdesc="A memory profiler for Python. It logs and plots the memory usage of all the variables."
arch=(any)
url="http://jmdana.github.io/memprof/"
license=('GPL')
groups=()
depends=("python" "python-matplotlib" "cython")
makedepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
install=
source=("https://pypi.python.org/packages/source/m/memprof/memprof-$pkgver.tar.gz")
md5sums=("f8a41a19e9bcb5c2a86373e95f252c6f")

package() {
  cd "$srcdir/$pypiname-$pkgver"
  python setup.py install --root="$pkgdir/" --optimize=1
}
