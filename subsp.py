import numpy as np


class Subspyce:
    def __init__(self, cec2017, fn_number, dim, probes_per_dimension, limit, min_dim, max_dim, initial_probe_count):
        self.dim = dim
        self.cec2017 = cec2017
        self.fn_number = fn_number
        self.probes_per_dimension = probes_per_dimension
        self.limit = limit
        self.initial_probe_count = initial_probe_count
        self.min_dim = min_dim
        self.max_dim = max_dim

    def optimize_min(self):
        available_samples = self.limit
        # probe the space
        sample_count = min(available_samples, self.initial_probe_count)
        available_samples -= sample_count
        samples = (np.random.uniform(size=self.dim) for _ in range(sample_count))

        # randomize initial set of points
        sample_fval_pairs = [(v, self.cec2017(self.fn_number, v)[0]) for v in samples]

        # choose the best one
        best = sample_fval_pairs[0]
        for pair in sample_fval_pairs[1:]:
            if pair[1] < best[1]:
                best = pair

        # optimize by iterating over collection
        # for dim in self.dim_subspaces
        while available_samples > 0:
            subspace_dim = np.random.randint(self.min_dim, self.max_dim + 1)
            # TODO: maybe probe count should depend on
            sample_count = min(available_samples, self.probes_per_dimension(subspace_dim))
            available_samples -= sample_count
            dimensions = np.random.choice(self.dim, size=subspace_dim, replace=False)
            for _ in range(sample_count):
                v = np.random.uniform(size=subspace_dim) * 200 - 100
                back_point = np.copy(best[0])
                for index, sub_dim in enumerate(dimensions):
                    back_point[sub_dim] = v[index]
                fv = self.cec2017(self.fn_number, back_point)[0]
                if fv < best[1]:
                    best = (back_point, fv)
