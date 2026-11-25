import { getUI } from '~/utils/i18n'

const GITHUB_RELEASE_BASE = 'https://github.com/razcreativestudio/razberry/releases/latest/download'
const GITHUB_RELEASES_PAGE = 'https://github.com/razcreativestudio/razberry/releases/latest'

/**
 * Returns the releases object, injecting checksums dynamically.
 * @param locale The locale to use for labels
 */
export function getReleasesWithChecksums(locale: string) {
  const {
    routes: {
      download: {
        links: { macos, windows, linux },
      },
    },
  } = getUI(locale)
  return (checksums: Record<string, string>) => {
    return {
      macos: {
        universal: {
          link: `${GITHUB_RELEASE_BASE}/razberry.macos-universal.dmg`,
          label: macos.universal,
          checksum: checksums['razberry.macos-universal.dmg'],
        },
      },
      windows: {
        x86_64: {
          link: `${GITHUB_RELEASE_BASE}/razberry.installer.exe`,
          label: windows['64bit'],
          checksum: checksums['razberry.installer.exe'],
        },
        arm64: {
          link: `${GITHUB_RELEASE_BASE}/razberry.installer-arm64.exe`,
          label: windows.ARM64,
          checksum: checksums['razberry.installer-arm64.exe'],
        },
      },
      linux: {
        x86_64: {
          tarball: {
            link: `${GITHUB_RELEASE_BASE}/razberry.linux-x86_64.tar.xz`,
            label: linux.x86_64,
            checksum: checksums['razberry.linux-x86_64.tar.xz'],
          },
        },
        aarch64: {
          tarball: {
            link: `${GITHUB_RELEASE_BASE}/razberry.linux-aarch64.tar.xz`,
            label: linux.aarch64,
            checksum: checksums['razberry.linux-aarch64.tar.xz'],
          },
        },
        flathub: {
          all: {
            link: GITHUB_RELEASES_PAGE,
            label: 'GitHub Releases (All Platforms)',
          },
        },
      },
    }
  }
}

export function getReleases(locale: string) {
  const {
    routes: {
      download: {
        links: { macos, windows, linux },
      },
    },
  } = getUI(locale)

  return {
    macos: {
      universal: {
        link: `${GITHUB_RELEASE_BASE}/razberry.macos-universal.dmg`,
        label: macos.universal,
      },
    },
    windows: {
      x86_64: {
        link: `${GITHUB_RELEASE_BASE}/razberry.installer.exe`,
        label: windows['64bit'],
      },
      arm64: {
        link: `${GITHUB_RELEASE_BASE}/razberry.installer-arm64.exe`,
        label: windows.ARM64,
      },
    },
    linux: {
      x86_64: {
        tarball: {
          link: `${GITHUB_RELEASE_BASE}/razberry.linux-x86_64.tar.xz`,
          label: linux.x86_64,
        },
      },
      aarch64: {
        tarball: {
          link: `${GITHUB_RELEASE_BASE}/razberry.linux-aarch64.tar.xz`,
          label: linux.aarch64,
        },
      },
      flathub: {
        all: {
          link: GITHUB_RELEASES_PAGE,
          label: 'GitHub Releases (All Platforms)',
        },
      },
    },
  }
}
