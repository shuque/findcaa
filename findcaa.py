#!/usr/bin/env python3
"""
findcaa.py - A script to find CAA records for DNS names.
See RFC 8659 for details.

Requires dnspython ("pip install dnspython").
"""

import argparse
import dns.resolver
import dns.name
import dns.rdatatype
import dns.flags

DEFAULT_TIMEOUT = 5 # seconds
DEFAULT_EDNS_BUFSIZE = 1232 # bytes


def get_resolver(addresses=None, dnssec_ok=False, checking_disabled=False,
                 timeout=DEFAULT_TIMEOUT, payload=DEFAULT_EDNS_BUFSIZE):
    """Return an appropriately configured Resolver object."""

    res = dns.resolver.Resolver()
    flags = dns.flags.RD | dns.flags.AD
    if checking_disabled:
        flags |= dns.flags.CD
    res.set_flags(flags)
    res.lifetime = timeout
    if dnssec_ok:
        res.use_edns(edns=0, ednsflags=dns.flags.DO, payload=payload)
    if addresses is not None:
        res.nameservers = addresses
    return res


def find_caa_records(name, resolver, verbose=False):
    """
    Find CAA records for a domain, searching upwards if needed.
    """

    current = dns.name.from_text(name)

    while current != dns.name.root:
        if verbose:
            print(f"Looking up CAA records for: {current}")
        try:
            rrset = resolver.resolve(current, 'CAA').rrset
            for rdata in rrset:
                print(rrset.name, rrset.ttl, dns.rdatatype.to_text(rrset.rdtype), rdata)
            return True
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer) as error:
            if verbose:
                print(f"No CAA records found for '{current}': {error}")
            current = current.parent()
            continue
        except Exception as error: # pylint: disable=broad-exception-caught
            print(f"An error occurred for '{current}': {error}")
            return False
    return False


def main():
    """Main function."""

    parser = argparse.ArgumentParser(
        description="Find CAA records for a DNS name (searches parent domains if needed)",
        prog="findcaa"
    )
    parser.add_argument("name", type=str, help="DNS name to lookup CAA records for")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose output showing search progress")
    parser.add_argument("--resolver", type=str,
                       help="IP address of DNS resolver to use")
    parser.add_argument("--cd", action="store_true",
                       help="Disable DNSSEC checking (set CD flag)")
    args = parser.parse_args()

    resolver_addresses = [args.resolver] if args.resolver else None
    resolver = get_resolver(addresses=resolver_addresses, checking_disabled=args.cd)
    if not find_caa_records(args.name, resolver, args.verbose):
        print(f"No CAA records found for '{args.name}'")


if __name__ == "__main__":
    main()
