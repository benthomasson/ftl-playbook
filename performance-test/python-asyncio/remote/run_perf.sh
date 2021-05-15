ulimit -Sn 10000
#Argtest

../../scripts/perf_test.py x x x x --only-header
for t in argtest
do
for n in 1 10 100 1000
do
../../scripts/perf_test.py "ftl-playbook -M modules -i inventory_remote1.yml playbook${n}.yml" ftl-playbook-remote ${t} ${n} --no-header
done
done
