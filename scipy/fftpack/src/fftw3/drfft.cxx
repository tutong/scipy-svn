/*
 * Last Change: Wed Aug 01 07:00 PM 2007 J
 *
 * RFFTW3 implementation
 *
 * Original code by Pearu Peterson.
 */

#if 0
GEN_CACHE(drfftw3, (int n, int d, int flags)
	  , int direction;
	  int flags;
	  fftw_plan plan;
	  double *ptr;, ((caches_drfftw3[i].n == n) &&
			 (caches_drfftw3[i].direction == d) &&
			 (caches_drfftw3[i].flags == flags))
	  , caches_drfftw3[id].direction = d;
	  caches_drfftw3[id].flags = flags;
	  caches_drfftw3[id].ptr =
	  (double *) fftw_malloc(sizeof(double) * (n));
	  caches_drfftw3[id].plan =
	  fftw_plan_r2r_1d(n, caches_drfftw3[id].ptr, caches_drfftw3[id].ptr,
			   (d > 0 ? FFTW_R2HC : FFTW_HC2R), flags);,
	  fftw_destroy_plan(caches_drfftw3[id].plan);
	  fftw_free(caches_drfftw3[id].ptr);, 10)
#endif

#include <new>
#include <cassert>

#include "common.h"

using namespace fft;

class RFFTW3Cache : public Cache<FFTW3CacheId> {
	public:	
		RFFTW3Cache(const FFTW3CacheId& id);
		virtual ~RFFTW3Cache();

		int compute_forward(double* inout) const
		{
                        assert (m_id.m_isalign ? is_simd_aligned(inout) : true);
			fftw_execute_r2r(m_plan, inout, m_wrk);
			COPYRFFTW2STD(m_wrk, inout, m_id.m_n);
			return 0;
		};

		int compute_backward(double* inout) const
		{
                        assert (m_id.m_isalign ? is_simd_aligned(inout) : true);
			COPYINVRFFTW2STD(inout, m_wrk, m_id.m_n);
			fftw_execute_r2r(m_plan, m_wrk, inout);
			return 0;
		};

	protected:
		fftw_plan m_plan;	
		double 	*m_wrk;	
		double 	*m_wrk2;	
};

RFFTW3Cache::RFFTW3Cache(const FFTW3CacheId& id)
:	Cache<FFTW3CacheId>(id)
{
        int flags = FFTW_MEASURE;

	m_wrk = (double*)fftw_malloc(id.m_n * sizeof(double) * 2);
	if (m_wrk == NULL) {
		goto fail_wrk;
	}

	m_wrk2 = (double*)fftw_malloc(id.m_n * sizeof(double) * 2);
	if (m_wrk2 == NULL) {
		goto clean_wrk;
	}

        if (!m_id.m_isalign) {
                flags |= FFTW_UNALIGNED;
        } 

	m_plan = fftw_plan_r2r_1d(id.m_n, m_wrk, m_wrk2, 
				  (id.m_dir > 0 ?  FFTW_R2HC:FFTW_HC2R), 
				  flags);

	if (m_plan == NULL) {
		goto clean_wrk2;
	}

	return ;

clean_wrk2:
	fftw_free(m_wrk2);
clean_wrk:
	fftw_free(m_wrk);
fail_wrk:
	throw std::bad_alloc();
}

RFFTW3Cache::~RFFTW3Cache()
{
	fftw_destroy_plan(m_plan);
	fftw_free(m_wrk2);
	fftw_free(m_wrk);
}

static CacheManager<FFTW3CacheId, RFFTW3Cache> fftw3_cmgr(10);

/* stub to make GEN_PUBLIC_API happy */
static void destroy_drfftw3_caches()
{
}

static void drfft_fftw3(double *inout, int n, int direction, int
			howmany, int normalize)
{
	int i;
	double *ptr = inout;

	RFFTW3Cache 	*cache;
        bool            isaligned;

        isaligned = is_simd_aligned(ptr); 

        if (howmany > 1) {
                /* 
                 * If executing for several consecutive buffers, we have to
                 * check that the shifting one buffer does not make it
                 * unaligned 
                 */
                isaligned = isaligned && is_simd_aligned(ptr + n);
        }

	cache = fftw3_cmgr.get_cache(FFTW3CacheId(n, direction, isaligned));

	switch (direction) {
	case 1:
		for (i = 0; i < howmany; ++i, ptr += n) {
			cache->compute_forward(ptr);
		}
		break;

	case -1:
		for (i = 0; i < howmany; ++i, ptr += n) {
			cache->compute_backward(ptr);
		}
		break;
	default:
		fprintf(stderr, "drfft: invalid direction=%d\n", direction);
	}

	if (normalize) {
		double d = 1.0 / n;
		ptr = inout;
		for (i = n * howmany - 1; i >= 0; --i) {
			(*(ptr++)) *= d;
		}
	}
}