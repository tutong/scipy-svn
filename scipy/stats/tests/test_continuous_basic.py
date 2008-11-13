import numpy.testing as npt
import numpy as np
import nose

from scipy import stats

"""
Test all continuous distributions.

Parameters were chosen for those distributions that pass the
Kolmogorov-Smirnov test.  This provides safe parameters for each
distributions so that we can perform further testing of class methods.

These tests currently check only/mostly for serious errors and exceptions,
not for numerically exact results.
"""

DECIMAL = 2 # specify the precision of the tests

distcont = [
    ['alpha', (3.5704770516650459,)],
    ['anglit', ()],
    ['arcsine', ()],
    ['beta', (2.3098496451481823, 0.62687954300963677)],
    ['betaprime', (100, 86)],
    ['bradford', (0.29891359763170633,)],
    ['burr', (0.94839838075366045, 4.3820284068855795)],
    ['cauchy', ()],
    ['chi', (78,)],
    ['chi2', (55,)],
    ['cosine', ()],
    ['dgamma', (1.1023326088288166,)],
    ['dweibull', (2.0685080649914673,)],
    ['erlang', (4, 0.7341136511570574, 0.047510038926818488)],
    ['expon', ()],
    ['exponpow', (2.697119160358469,)],
    ['exponweib', (2.8923945291034436, 1.9505288745913174)],
    ['f', (29, 18)],
    ['fatiguelife', (29, 18)],
    ['fisk', (3.0857548622253179,)],
    ['foldcauchy', (4.7164673455831894,)],
    ['foldnorm', (1.9521253373555869,)],
    ['frechet_l', (3.6279911255583239,)],
    ['frechet_r', (1.8928171603534227,)],
    ['gamma', (1.9932305483800778,)],
    ['gausshyper', (13.763771604130699, 3.1189636648681431,
                    2.5145980350183019, 5.1811649903971615)],
    ['genexpon', (9.1325976465418908, 16.231956600590632, 3.2819552690843983)],
    ['genextreme', (3.3184017469423535,)],
    ['gengamma', (4.4162385429431925, 3.1193091679242761)],
    ['genhalflogistic', (0.77274727809929322,)],
    ['genlogistic', (0.41192440799679475,)],
    ['genpareto', (4.4566867037959144,)],
    ['gilbrat', ()],
    ['gompertz', (0.94743713075105251,)],
    ['gumbel_l', ()],
    ['gumbel_r', ()],
    ['halfcauchy', ()],
    ['halflogistic', ()],
    ['halfnorm', ()],
    ['hypsecant', ()],
    ['invgamma', (2.0668996136993067,)],
    ['invnorm', (0.14546264555347513,)],
    ['invweibull', (0.58847112119264788,)],
    ['johnsonsb', (4.3172675099141058, 3.1837781130785063)],
    ['johnsonsu', (2.554395574161155, 2.2482281679651965)],
    ['ksone', (22,)],  # new added
    ['kstwobign', ()],
    ['laplace', ()],
    ['levy', ()],
    ['levy_l', ()],
#    ['levy_stable', (0.35667405469844993,
#                     -0.67450531578494011)], #NotImplementedError
    ['loggamma', (0.41411931826052117,)],
    ['logistic', ()],
    ['loglaplace', (3.2505926592051435,)],
    ['lognorm', (0.95368226960575331,)],
    ['lomax', (1.8771398388773268,)],
    ['maxwell', ()],
    ['mielke', (4.6420495492121487, 0.59707419545516938)],
    ['nakagami', (4.9673794866666237,)],
    ['ncf', (27, 27, 0.41578441799226107)],
    ['nct', (14, 0.24045031331198066)],
    ['ncx2', (21, 1.0560465975116415)],
    ['norm', ()],
    ['pareto', (2.621716532144454,)],
    ['powerlaw', (1.6591133289905851,)],
    ['powerlognorm', (2.1413923530064087, 0.44639540782048337)],
    ['powernorm', (4.4453652254590779,)],
    ['rayleigh', ()],
    ['rdist', (3.8266985793976525,)],
    ['recipinvgauss', (0.63004267809369119,)],
    ['reciprocal', (0.0062309367010521255, 1.0062309367010522)],
    ['rice', (0.7749725210111873,)],
    ['semicircular', ()],
    ['t', (2.7433514990818093,)],
    ['triang', (0.15785029824528218,)],
    ['truncexpon', (4.6907725456810478,)],
    ['truncnorm', (-1.0978730080013919, 2.7306754109031979)],
    ['tukeylambda', (3.1321477856738267,)],
    ['uniform', ()],
    ['vonmises', (3.9939042581071398,)],
    ['wald', ()],
    ['weibull_max', (2.8687961709100187,)],
    ['weibull_min', (1.7866166930421596,)],
    ['wrapcauchy', (0.031071279018614728,)]]


def test_cont_basic():
    for distname, arg in distcont[:]:
        distfn = getattr(stats, distname)
        rvs = distfn.rvs(size=1000,*arg)
        sm = rvs.mean()
        sv = rvs.var()
        skurt = stats.kurtosis(rvs)
        sskew = stats.skew(rvs)
        yield check_sample_meanvar_, distfn, arg, sm, sv, distname + \
              'sample mean test'
        yield check_sample_skew_kurt, distfn, arg, skurt, sskew, distname
        yield check_cdf_ppf, distfn, arg, distname
        yield check_sf_isf, distfn, arg, distname
        yield check_pdf, distfn, arg, distname
        #yield check_oth, distfn, arg # is still missing


def check_sample_meanvar_(distfn, arg, sm, sv, msg):
    m,v = distfn.stats(*arg)
    check_sample_meanvar, sm, m, msg + 'sample mean test'
    check_sample_meanvar, sv, v, msg + 'sample var test'

def check_sample_skew_kurt(distfn, arg, sk, ss, msg):
    k,s = distfn.stats(moment='ks',*arg)
    check_sample_meanvar, sk, k, msg + 'sample skew test'
    check_sample_meanvar, ss, s, msg + 'sample kurtosis test'

def check_sample_meanvar(sm,m,msg):

    if m < np.inf:
        npt.assert_almost_equal(sm, m, decimal=DECIMAL, err_msg= msg + \
                                ' - finite moment')
    else:
        assert sm > 10000, 'infinite moment, sm = ' + str(sm)

def check_cdf_ppf(distfn,arg,msg):
    npt.assert_almost_equal(distfn.cdf(distfn.ppf([0.1,0.5,0.9], *arg), *arg),
                            [0.1,0.5,0.9], decimal=DECIMAL, err_msg= msg + \
                            ' - cdf-ppf roundtrip')

def check_sf_isf(distfn,arg,msg):
    npt.assert_almost_equal(distfn.sf(distfn.isf([0.1,0.5,0.9], *arg), *arg),
                            [0.1,0.5,0.9], decimal=DECIMAL, err_msg= msg + \
                            ' - sf-isf roundtrip')
    npt.assert_almost_equal(distfn.cdf([0.1,0.9], *arg),
                            1.0-distfn.sf([0.1,0.9], *arg),
                            decimal=DECIMAL, err_msg= msg + \
                            ' - cdf-sf relationship')

def check_pdf(distfn, arg, msg):
    median = distfn.ppf(0.5, *arg)
    eps = 1e-6
    pdfv = distfn.pdf(median, *arg)
    if (pdfv < 1e-4) or (pdfv > 1e4):
        # avoid checking a case where pdf is close to zero or huge (singularity)
        median = median + 0.1
        pdfv = distfn.pdf(median, *arg)
    cdfdiff = (distfn.cdf(median + eps, *arg) -
               distfn.cdf(median - eps, *arg))/eps/2.0
    #replace with better diff and better test (more points)
    npt.assert_almost_equal(pdfv, cdfdiff,
                decimal=DECIMAL, err_msg= msg + ' - cdf-pdf relationship')

distmissing = ['wald', 'gausshyper', 'genexpon', 'rv_continuous',
    'loglaplace', 'rdist', 'semicircular', 'invweibull', 'ksone',
    'cosine', 'kstwobign', 'truncnorm', 'mielke', 'recipinvgauss', 'levy',
    'johnsonsu', 'levy_l', 'powernorm', 'wrapcauchy',
    'johnsonsb', 'truncexpon', 'rice', 'invnorm', 'invgamma',
    'powerlognorm']

def test_missing_distributions():
    #test from scipy.stats.tests
    for dist, args in distcont:
        distfunc = getattr(stats, dist)
        alpha = 0.01
        yield check_distribution, dist, args, alpha


def check_distribution(dist, args, alpha):
    #test from scipy.stats.tests
    D,pval = stats.kstest(dist,'', args=args, N=1000)
    if (pval < alpha):
        D,pval = stats.kstest(dist,'',args=args, N=1000)
        assert (pval > alpha), "D = " + str(D) + "; pval = " + str(pval) + \
               "; alpha = " + str(alpha) + "\nargs = " + str(args)

if __name__ == "__main__":
    nose.run(argv=['', __file__])

