# findcaa
Find relevant CAA record set for a domain name

## Pre-requisites

* dnspython package

```
pip install dnspython
```

## Help string

```
usage: findcaa [-h] [-v] [--resolver RESOLVER] [--cd] name

Find CAA records for a DNS name (searches parent domains if needed)

positional arguments:
  name                 DNS name to lookup CAA records for

optional arguments:
  -h, --help           show this help message and exit
  -v, --verbose        Enable verbose output showing search progress
  --resolver RESOLVER  IP address of DNS resolver to use
  --cd                 Disable DNSSEC checking (set CD flag)
```

## Example Usage

```
$ findcaa.py myfss.us.af.mil
us.af.mil. 500 CAA 0 issue "digicert.com"
us.af.mil. 500 CAA 0 issue "identrust.com"
```

Verbose mode (-v):

```
$ findcaa.py -v xxx.myfss.us.af.mil
Looking up CAA records for: xxx.myfss.us.af.mil.
No CAA records found for 'xxx.myfss.us.af.mil.': The DNS query name does not exist: xxx.myfss.us.af.mil., trying parent domain
Looking up CAA records for: myfss.us.af.mil.
No CAA records found for 'myfss.us.af.mil.': The DNS response does not contain an answer to the question: myfss.us.af.mil. IN CAA, trying parent domain
Looking up CAA records for: us.af.mil.
us.af.mil. 277 CAA 0 issue "digicert.com"
us.af.mil. 277 CAA 0 issue "identrust.com"
```
