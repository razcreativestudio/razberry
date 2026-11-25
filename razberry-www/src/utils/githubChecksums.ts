import { CONSTANT } from '~/constants'

type GitHubAsset = {
  name: string
  digest?: string
}

/**
 * Fetches the latest release assets from GitHub (razcreativestudio/razberry)
 * and extracts their checksums safely with fallback.
 */
export async function getChecksums() {
  if (import.meta.env.DEV) {
    return CONSTANT.CHECKSUMS
  }
  try {
    const res = await fetch('https://api.github.com/repos/razcreativestudio/razberry/releases/latest', {
      headers: {
        Accept: 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'razberry-browser-checksum-fetcher',
      },
    })
    if (!res.ok) return CONSTANT.CHECKSUMS
    const data = await res.json()
    const assets = (data.assets ?? []) as GitHubAsset[]

    const checksums: Record<string, string> = {}
    for (const asset of assets) {
      if (asset.digest) {
        checksums[asset.name] = asset.digest
      }
    }
    return Object.keys(checksums).length > 0 ? checksums : CONSTANT.CHECKSUMS
  } catch {
    return CONSTANT.CHECKSUMS
  }
}
